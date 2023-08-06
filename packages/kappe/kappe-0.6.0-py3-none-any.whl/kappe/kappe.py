"""
Convert mcap (ROS1 & ROS2) files.

Message definitions:
    Message definitions are read from ROS and disk ./msgs/
    git clone --depth=1 --branch=humble https://github.com/ros2/common_interfaces.git msgs
"""

import argparse
import logging
from multiprocessing import Pool, RLock
from pathlib import Path
from typing import Any

import yaml
from tqdm import tqdm

from kappe import __version__
from kappe.convert import Converter
from kappe.cut import CutSettings, cutter
from kappe.plugin import load_plugin
from kappe.settings import Settings


class TqdmLoggingHandler(logging.Handler):
    def emit(self, record: Any):
        try:
            msg = self.format(record)
            tqdm.write(msg)
            self.flush()
        except Exception:  # noqa: BLE001
            self.handleError(record)


logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)-7s | %(name)s | %(message)s',
    datefmt='%H:%M:%S',
    handlers=[TqdmLoggingHandler()],
)

logger = logging.getLogger(__name__)


def worker(arg: tuple[Path, Path, Settings, int]):
    # TODO: dataclass
    input_path, output_path, config, tqdm_idx = arg

    logger.info('Writing %s', output_path)
    try:
        conv = Converter(config, input_path, output_path)
        conv.process_file(tqdm_idx)
        conv.finish()

    except KeyboardInterrupt:
        logger.info('WORKER: Keyboard interrupt')
        return
    except Exception:
        logger.exception('Failed to convert %s', input_path)

    logger.info('Done    %s', output_path)


def process(config: Settings, input_path: Path, output_path: Path, *, overwrite: bool) -> None:
    tasks: list[tuple[Path, Path, Settings, int]] = []

    # TODO: make more generic
    if input_path.is_file():
        mcap_out = output_path / input_path.name
        if mcap_out.exists() and not overwrite:
            logger.info('File exists: %s -> skipping', mcap_out)
        else:
            tasks.append((input_path, mcap_out, config, 0))
    else:
        for idx, mcap_in in enumerate(input_path.rglob('**/*.mcap')):
            mcap_out = output_path / mcap_in.relative_to(input_path.parent)

            if mcap_out.exists() and not overwrite:
                logger.info('File exists: %s -> skipping', mcap_out)
                continue
            tasks.append((mcap_in, mcap_out, config, idx))

    logger.info('Using %d threads', config.general.threads)
    tqdm.set_lock(RLock())  # for managing output contention

    pool = None
    try:
        pool = Pool(min(config.general.threads, len(tasks)),
                    initializer=tqdm.set_lock, initargs=(tqdm.get_lock(),))
        pool.map(worker, tasks)
    except KeyboardInterrupt:
        logger.info('Keyboard interrupt')
    finally:
        if pool is not None:
            pool.terminate()
            pool.join()


def cmd_convert(args: argparse.Namespace):
    if args.config is None:
        config = Settings()
    else:
        with args.config.open(encoding='utf-8') as f:
            config_text = f.read()
        config_yaml = yaml.safe_load(config_text)
        config = Settings(**config_yaml)

    # check for msgs folder
    if config.msg_folder is not None and not config.msg_folder.exists():
        logger.error('msg_folder does not exist: %s', config.msg_folder)
        config.msg_folder = None

    errors = False

    for conv in config.plugins:
        try:
            load_plugin(config.plugin_folder, conv.name)
            continue
        except ValueError:
            pass

        errors = True
        logger.error('Failed to load plugin: %s', conv.name)

    input_path: Path = args.input
    if not input_path.exists():
        raise FileNotFoundError(f'Input path does not exist: {input_path}')

    output_path: Path = args.output

    if errors:
        logger.error('Errors found, aborting')
    else:
        process(config, input_path, output_path, overwrite=args.overwrite)


def cmd_cut(args: argparse.Namespace):
    logger.info('cut')

    config_text = args.config.read()
    config_yaml = yaml.safe_load(config_text)
    config = CutSettings(**config_yaml)

    cutter(args.input, args.output, config)


def main() -> None:
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        fromfile_prefix_chars='@',
    )

    parser.add_argument('--verbose', action='store_true', help='Verbose output')
    parser.add_argument('--version', action='version', version=__version__)

    sub = parser.add_subparsers(
        title='subcommands',
        required=True,
    )

    cutter = sub.add_parser('cut')
    cutter.set_defaults(func=cmd_cut)

    cutter.add_argument('input', type=Path, help='input file')
    cutter.add_argument(
        'output',
        type=Path,
        help='output folder, default: ./cut_out',
        default=Path('./cut_out'),
        nargs='?')
    cutter.add_argument('--config', type=argparse.FileType(), help='config file', required=True)
    cutter.add_argument(
        '--overwrite',
        action='store_true',
        help='Overwrite existing files')

    convert = sub.add_parser('convert')
    convert.set_defaults(func=cmd_convert)

    convert.add_argument('input', type=Path, help='input folder')
    convert.add_argument('output', type=Path, help='output folder')
    convert.add_argument('--config', type=Path, help='config file')
    convert.add_argument(
        '--overwrite',
        action='store_true',
        help='Overwrite existing files')

    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    args.func(args)


if __name__ == '__main__':
    main()
