#!/usr/bin/env python
"""
Custom test runner

If args or options, we run the testsuite as quickly as possible.

If args but no options, we default to using the spec plugin and aborting on
first error/failure.

If options, we ignore defaults and pass options onto Nose.

Examples:

Run all tests (as fast as possible)
$ ./runtests.py

Run all unit tests (using spec output)
$ ./runtests.py tests/unit

Run all books unit tests (using spec output)
$ ./runtests.py tests/unit/books

Run all tests relating to books
$ ./runtests.py --attr=books

Re-run failing tests (needs to be run twice to first build the index)
$ ./runtests.py ... --failed

Drop into pdb when a test fails
$ ./runtests.py ... --pdb-failures
"""
import os
import sys

import django
from django_nose import NoseTestSuiteRunner

import logging
# No logging
logging.disable(logging.CRITICAL)


def run_tests(verbosity, *args):
    test_runner = NoseTestSuiteRunner(verbosity=verbosity)
    if not args:
        args = ['tests']
    failures = test_runner.run_tests(args)
    sys.exit(bool(failures))

if __name__ == '__main__':
  os.environ['DJANGO_SETTINGS_MODULE'] = 'tests.settings'
  django.setup()
  
  args = sys.argv[1:]
  
  verbosity = 0
  run_tests(verbosity, *args)
#   
#     args = sys.argv[1:]
# 
#     verbosity = 1
#     if not args:
#         # If run with no args, try and run the testsuite as fast as possible.
#         # That means across all cores and with no high-falutin' plugins.
#         import multiprocessing
#         try:
#             num_cores = multiprocessing.cpu_count()
#         except NotImplementedError:
#             num_cores = 4  # Guess
#         args = ['--ipdb',
#                 '--nocapture',
#                 '--stop',
#                 '--processes=%s' % num_cores]
#     else:
#         # Some args/options specified.  Check to see if any nose options have
#         # been specified.  If they have, then don't set any
#         has_options = any(map(lambda x: x.startswith('--'), args))
#         if not has_options:
#             # Default options:
#             # --stop Abort on first error/failure
#             # --nocapture Don't capture STDOUT
#             args.extend(['--ipdb',
#                          '--nocapture',
#                          '--stop',
#                          '--with-specplugin'])
#         else:
#             # Remove options as nose will pick these up from sys.argv
#             for arg in args:
#                 if arg.startswith('--verbosity'):
#                     verbosity = int(arg[-1])
#             args = [arg for arg in args if not arg.startswith('-')]
# 
#     configure()
#     django.setup()
#     run_tests(verbosity, *args)

