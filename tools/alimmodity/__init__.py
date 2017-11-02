# coding=utf-8
from __future__ import absolute_import
import argparse

from .main import convert


__version_info__ = ('0', '1', '0')
__version__ = '.'.join(__version_info__)


def command_options():

    parser = argparse.ArgumentParser(
        description='Options of run Alimmodity.')

    parser.add_argument('-v', '--version',
                        dest='version',
                        action='store_const',
                        const=True,
                        help='Show current version.')

    # Server
    parser.add_argument('-c', '--csv',
                        dest='csv_path',
                        action='store',
                        nargs='?',
                        type=str,
                        const=None,
                        required=True,
                        help='Define csv file path.')

    parser.add_argument('-o', '--output',
                        dest='output_path',
                        action='store',
                        nargs='?',
                        type=str,
                        const=None,
                        help='Define output json file path.')

    opts, unknown = parser.parse_known_args()

    return opts


def run():
    opts = command_options()
    if opts.version:
        print 'Alimmodity:', __version__
    elif opts.csv_path:
        convert(opts.csv_path, opts.output_path)
