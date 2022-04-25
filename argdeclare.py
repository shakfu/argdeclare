"""cli: general commandline interface module

Provides a declarative argparse-based class to be inherited
by applications wishing to provide a basic commandline interface.

This is based on my old `argdeclare` code
    see: http://code.activestate.com/recipes/576935-argdeclare-declarative-interface-to-argparse


TODO:
-----

- make fully recursive! 

like haskell:

    sum :: (Num a) => [a] -> a  
    sum [] = 0  
    sum (x:xs) = x + sum' xs  

concept is

    parse [] = 0
    parse (x:xs) = 
        if x in structure:
            structure[x] = options[x]
        else:
            structure[x] = dummy[x]
        structure[x].children.append(xs)
        parse(xs)
"""
import argparse
import sys
import inspect

# ------------------------------------------------------------------------------
# Generic utility functions and classes for commandline ops


# option decorator
def option(*args, **kwds):
    """decorator to provide an argparse option to a method."""

    def _decorator(func):
        _option = (args, kwds)
        if hasattr(func, "options"):
            func.options.append(_option)
        else:
            func.options = [_option]
        return func

    return _decorator


# arg decorator
arg = option


# combines option decorators
def option_group(*options):
    """Collection of options to simplify common options reuse."""

    def _decorator(func):
        for opt in options:
            func = opt(func)
        return func

    return _decorator


class MetaCommander(type):
    """Metaclass to provide argparse boilerplate features to its instance class"""

    def __new__(cls, classname, bases, classdict):
        subcmds = {}
        for name, func in list(classdict.items()):
            if name.startswith("do_"):
                name = name[3:]
                subcmd = {
                    "name": name,
                    "func": func,
                    "options": [],
                }
                if hasattr(func, "options"):
                    subcmd["options"] = func.options
                subcmds[name] = subcmd
        classdict["_argparse_subcmds"] = subcmds
        return type.__new__(cls, classname, bases, classdict)


class Commander(metaclass=MetaCommander):
    """app: description here"""

    name = "app name"
    epilog = ""
    version = "0.1"
    default_args = ["--help"]
    _argparse_subcmds: dict  # just to silence static checkers
    _argparse_levels: int = 0  # how many subcommand levels to create
    _argparse_structure: dict = {}


    def add_parser(self, subparsers, subcmd, name=None):
        if not name:
            name = subcmd["name"]
        subparser = subparsers.add_parser(name, help=subcmd["func"].__doc__)

        for args, kwds in subcmd["options"]:
            subparser.add_argument(*args, **kwds)
        subparser.set_defaults(func=subcmd["func"])
        return subparser

    def parse_subparsers(self, subparsers, subcmd, name):
        head, *tail = name.split("_")

        if not tail:  # i.e head == name
            # scenario: single section name and subcmd is given
            subparser = self.add_parser(subparsers, subcmd)
            if head not in self._argparse_structure:
                self._argparse_structure[head] = subparser.add_subparsers(
                    title=f"{head} subcommands",
                    description=subcmd["func"].__doc__,
                    help="additional help",
                    metavar="",
                )
        else:
            if head in self._argparse_structure:
                _subparsers = self._argparse_structure[head]
                subparser = self.add_parser(_subparsers, subcmd, name="_".join(tail))
            else:
                # create a dummy 'head' if it wasn't created manually
                subcmd = {
                    'name': head,
                    'func': lambda self, args: subparser.print_help(),
                    'options': [],
                }
                subcmd['func'].__doc__ = f"{head} commands"
                subparser = self.add_parser(subparsers, subcmd, name=head)

                # add it to structure
                self._argparse_structure[head] = subparser.add_subparsers(
                    title=f"{head} subcommands",
                    description=subcmd['func'].__doc__,
                    help='additional help',
                    metavar='',
                )

                # add tail as a child to it
                _subparsers = self._argparse_structure[head]
                # self.parse_subparsers(_subparsers, subcmd, name="_".join(tail))
                subparser = self.add_parser(_subparsers, subcmd, name="_".join(tail))


    def cmdline(self):
        """Main commandline function to process commandline arguments and options."""
        parser = argparse.ArgumentParser(
            # prog = self.name,
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
            description=self.__doc__,
            epilog=self.epilog,
        )

        parser.add_argument(
            "-v", "--version", action="version", version="%(prog)s " + self.version
        )

        ## default arg
        # parser.add_argument('db', help='arg')
        # parser.add_argument('--db', help='option')

        # non-subcommands here

        subparsers = parser.add_subparsers(
            title="subcommands",
            description="valid subcommands",
            help="additional help",
            metavar="",
        )

        for name in sorted(self._argparse_subcmds.keys()):  # pylint: disable=E1101
            # print('name:', name)
            subcmd = self._argparse_subcmds[name]  # pylint: disable=E1101
            if not self._argparse_levels:
                subparser = self.add_parser(subparsers, subcmd)
            else:
                self.parse_subparsers(subparsers, subcmd, name)

        if len(sys.argv) <= 1:
            options = parser.parse_args(self.default_args)
        else:
            options = parser.parse_args()
        options.func(self, options)
