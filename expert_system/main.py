import sys
import logging
from expert_system.ExpertSystem import ExpertSystem

logging.basicConfig()

def main(argc, argv):
    try:
        if argc != 2:
            print('Using: python3.6 -m expert_system.main <filename>')
            sys.exit(1)
        with open(argv[1]) as f:
            content = f.read()
        logging.debug(f'content start (stripped)')
        logging.debug(f'\n{content.strip()}')
        logging.debug(f'content end')
        es = ExpertSystem()
        res = es.resolve(content)
        for k,v in res.items():
            print(f'{k} is {v}')
    except Exception as e:
        print(e)

if __name__ == '__main__':
    main(len(sys.argv), sys.argv)
