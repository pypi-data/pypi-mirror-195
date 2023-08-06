from .nfscrapy import run
from krx_hj3415 import krx
from util_hj3415 import utils
import argparse


def nfscraper():
    spiders = ['c101', 'c106', 'c103', 'c104']

    parser = argparse.ArgumentParser()
    parser.add_argument('spider', help=f"Spiders - {spiders}")
    parser.add_argument('target', help="Target for scraping (type 6digit code or 'all')")

    parser.add_argument('-d', '--db_path', help="Set mongo database path")
    args = parser.parse_args()

    if args.spider in spiders:
        if args.spider == 'c101':
            if args.target == 'all':
                run.c101(krx.get_codes(), args.db_path) if args.db_path else run.c101(krx.get_codes())
            elif utils.is_6digit(args.target):
                run.c101([args.target, ], args.db_path) if args.db_path else run.c101([args.target, ])
        if args.spider == 'c103':
            if args.target == 'all':
                x = input("It will take a long time. Are you sure? (y/N)")
                if x == 'y' or x == 'Y':
                    run.c103(krx.get_codes(), args.db_path) if args.db_path else run.c103(krx.get_codes())
            elif utils.is_6digit(args.target):
                run.c103([args.target, ], args.db_path) if args.db_path else run.c103([args.target, ])
        if args.spider == 'c104':
            if args.target == 'all':
                x = input("It will take a long time. Are you sure? (y/N)")
                if x == 'y' or x == 'Y':
                    run.c104(krx.get_codes(), args.db_path) if args.db_path else run.c104(krx.get_codes())
            elif utils.is_6digit(args.target):
                run.c104([args.target, ], args.db_path) if args.db_path else run.c104([args.target, ])
        if args.spider == 'c106':
            if args.target == 'all':
                run.c106(krx.get_codes(), args.db_path) if args.db_path else run.c106(krx.get_codes())
            elif utils.is_6digit(args.target):
                run.c106([args.target, ], args.db_path) if args.db_path else run.c106([args.target, ])
    else:
        print(f"The spider option should be in {spiders}")


if __name__ == '__main__':
    nfscraper()
