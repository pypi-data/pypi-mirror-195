""" __main__ """

import sys
from wwvb import wwvb

def main(args=None):
    """ WWVB API via command line """
    if args is None:
        args = sys.argv[1:]
    wwvb.wwvb(args)

if __name__ == '__main__':
    main()
