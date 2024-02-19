# argdeclare

Declarative methods to use with argparse

## Declarative Format Example

```python
#!/usr/bin/env python3

from argdeclare import Commander, option, option_group

# ----------------------------------------------------------------------------
# Commandline interface

common_options = option_group(
    option("--dump", action="store_true", help="dump project and product vars"),
    option("-d","--download",
           action="store_true",
           help="download python build/downloads"),
    option("-r", "--reset", action="store_true", help="reset python build"),
    option("-i","--install",
           action="store_true",
           help="install python to build/lib"),
    option("-b","--build",
           action="store_true",
           help="build python in build/src"),
    option("-c","--clean",
           action="store_true",
           help="clean python in build/src"),
    option("-z", "--ziplib", action="store_true", help="zip python library"),
    option("-p", "--py-version", type=str,
           help="set required python version to download and build"),
)

class Application(Commander):
    """builder: builds the py-js max external and python from source."""
    name = 'builder'
    epilog = ''
    version = '0.1'
    default_args = ['--help']
    _argparse_levels = 1


# ----------------------------------------------------------------------------
# python builder methods

    # def do_python(self, args):
    #     "download and build python from src"

    @common_options
    def do_python_static(self, args):
        """build static python"""
        print(args)

    @common_options
    def do_python_shared(self, args):
        """build shared python"""
        print(args)

    @common_options
    def do_python_shared_pkg(self, args):
        """build shared python to embed in package"""
        print(args)

    @common_options
    def do_python_framework(self, args):
        """build framework python"""
        print(args)

    @common_options
    def do_python_framework_pkg(self, args):
        """build framework python to embed in a package"""
        print(args)


# ----------------------------------------------------------------------------
# utility methods

    # def do_check(self, args):
    #     """check reference utilities"""
    #     print(args)

    @common_options    
    def do_check_log_day(self, args):
        """analyze log day"""
        print(args)

    @common_options    
    def do_check_log_week(self, args):
        """analyze log week"""
        print(args)

    @common_options
    def do_check_sys_month(self, args):
        """analyze sys month"""
        print(args)

    @common_options
    def do_check_sys_def(self, args):
        """analyze sys def"""
        print(args)

    @common_options
    def do_check_sys_xyz(self, args):
        """analyze sys xyz"""
        print(args)

    @common_options
    def do_test(self, args):
        """test suite"""
        print(args)


    @common_options
    def do_test_app(self, args):
        """test app"""
        print(args)

    @common_options
    def do_test_functions(self, args):
        """test functions"""
        print(args)

if __name__ == '__main__':
    app = Application()
    app.cmdline()
```

`with levels=0` gives:


```text
$ python3 demo.py
usage: demo.py [-h] [-v]  ...

builder: builds the py-js max external and python from source.

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit

subcommands:
  valid subcommands

                        additional help
    check_log_day       analyze log day
    check_log_week      analyze log week
    check_sys_def       analyze sys def
    check_sys_month     analyze sys month
    check_sys_xyz       analyze sys xyz
    python_framework    build framework python
    python_framework_pkg
                        build framework python to embed in a package
    python_shared       build shared python
    python_shared_pkg   build shared python to embed in package
    python_static       build static python
    test                test suite
    test_app            test app
    test_functions      test functions
```

`with levels=1` gives:

```text

$ python3 demo.py
usage: demo.py [-h] [-v]  ...

builder: builds the py-js max external and python from source.

optional arguments:
  -h, --help     show this help message and exit
  -v, --version  show program's version number and exit

subcommands:
  valid subcommands

                 additional help
    check        check commands
    python       python commands
    test         test suite
```