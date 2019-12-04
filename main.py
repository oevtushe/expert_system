#!/usr/bin/python3.6

import sys
import logging
from ExpertSystem import ExpertSystem

logging.basicConfig(level=logging.DEBUG)

def main(argc, argv):
    with open(argv[1]) as f:
        content = f.read()
    logging.debug(f'content start')
    logging.debug(f'\n{content}')
    logging.debug(f'content end')
    es = ExpertSystem(content)
    es.resolve()

if __name__ == '__main__':
    main(len(sys.argv), sys.argv)
