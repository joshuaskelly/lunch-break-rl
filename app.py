import argparse
import sys

import game


class Parser(argparse.ArgumentParser):
    """Simple wrapper class to provide help on error"""
    def error(self, message):
        sys.stderr.write('error: %s\n' % message)
        self.print_help()
        sys.exit(1)


class ArgHelper(object):
    """Helper class to lazily handle command line arguments. The available 
    arguments will be inferred from actual arguments passed. If an 
    argument is followed by a value it will be treated as a sting. Otherwise,
    it will be treated as a flag.
    """
    def __init__(self):
        parser = Parser(prog='lunch break rl')
        _, unknown_args = parser.parse_known_args()

        for i, arg in enumerate(unknown_args):
            # Only add arguments
            if arg.startswith(('-', '--')):
                next_is_value = False
                if i + 1 < len(unknown_args):
                    next_is_value = not unknown_args[i + 1].startswith(('-', '--'))

                # If argument is followed by a value, add it as a vanilla
                # argument.
                if next_is_value:
                    parser.add_argument(arg)

                # Otherwise add it as a flag
                else:
                    parser.add_argument(arg, action='store_true')

        self._args = parser.parse_args().__dict__

    def __getattr__(self, item):
        return self._args.get(item)


if __name__ == '__main__':
    arg = ArgHelper()
    g = game.Game(arg)
    g.run()
