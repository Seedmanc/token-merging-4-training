import argparse

parser = argparse.ArgumentParser()
parser.add_argument('captions_path', nargs='?', help='Required.')
parser.add_argument("--dry", action="store_true", help='Don\'t change the files')
parser.add_argument("--author",  help='Replace author tag with --class-tokens + " style"')
parser.add_argument("--class-tokens",  help='Replace --author tag with this. Defaults to --author w/o spaces or (...). '
                                            'Use --class-tokens=  to remove author entirely.')
group = parser.add_mutually_exclusive_group()
group.add_argument("--brief", action="store_true", help='Reduce console spam')
group.add_argument("--verbose", action="store_true")

args = parser.parse_known_args()[0]

if args.captions_path is None:
    parser.print_help() #dumb pytest forces me to use this nonsense instead of making captions required