import argparse
from .auto_detect import start_auto_detect

def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()
    parser_nita = subparsers.add_parser('nita')
    parser_nita.set_defaults(handler=nita)

    args = parser.parse_args()
    if hasattr(args, 'handler'):
        args.handler(args)
    else:
        parser.print_help()

def nita(args):
    start_auto_detect()

if __name__ == "__main__":
    main()
