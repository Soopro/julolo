# coding=utf-8
from __future__ import absolute_import
import argparse

from .main import convert


__version_info__ = ('0', '2', '3')
__version__ = '.'.join(__version_info__)


def command_options():

    parser = argparse.ArgumentParser(
        description='Options of run Alimmodity.')

    parser.add_argument('-v', '--version',
                        dest='version',
                        action='store_const',
                        const=True,
                        help='Show current version.')

    parser.add_argument('-c', '--csv',
                        dest='csv_path',
                        action='store',
                        nargs='?',
                        type=str,
                        const=None,
                        required=True,
                        help='Define csv file path.')

    parser.add_argument('-o', '--output',
                        dest='output_dir',
                        action='store',
                        nargs='?',
                        type=str,
                        const=None,
                        help='Define output to dir.')

    parser.add_argument('-p', '--policy',
                        dest='policy_path',
                        action='store',
                        nargs=1,
                        type=str,
                        default='policy.json',
                        help='Define policy file path (json).')

    opts, unknown = parser.parse_known_args()

    return opts


def run():
    opts = command_options()
    if opts.version:
        print 'Alimmodity:', __version__
    elif opts.csv_path:
        convert(csv_path=opts.csv_path,
                output_dir=opts.output_dir,
                policy_path=opts.policy_path)
