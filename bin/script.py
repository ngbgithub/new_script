#!/usr/bin/env python

'''Do X.
'''

from __future__ import print_function

import logging, os.path, sys
import new_script.boilerplate as boilerplate

PACKAGE_NAME = 'new_script'
INSTALL_PREFIX = os.path.abspath(os.path.join(sys.path[0], '..'))
CONF_DIR = os.path.join(INSTALL_PREFIX, 'etc', PACKAGE_NAME)

# Note that the logger has to be configured before importing any other
#   custom modules, or logging won't work for them.
boilerplate.configureLogger(os.path.join(CONF_DIR, 'logging.conf'))
logger = logging.getLogger('main')


def main():
    '''This is the function that is executed when the script is called
    from the command line.
    '''
    import new_script.boilerplate as boilerplate
    emitTrace = True
    try:
        args = readCommandLine() # This may spit out a help message and quit.
        emitTrace = args.with_trace
        logger.info('Initializing...')
        boilerplate.logArgs(args)

        logger.info('Program complete.')

    except Exception as e:
        boilerplate.manageException(e, emitTrace)


def readCommandLine():
    '''Deal with the command line.
    '''
    import argparse

    parser = argparse.ArgumentParser(description=__doc__)

    class Default:
        def __init__(self):
            self.with_trace = False
            self.products = [100,]
    d = Default()

    parser.add_argument('-t', '--with-trace', action='store_true',
                        default=d.with_trace,
                        help='Emit a full trace upon encountering an error.')

    parser.add_argument('--products', metavar=('XXXX', 'YYYY'), type=int,
                        default=d.products, nargs='+', help='Specify the'
                        ' relevant product types. (default: {d})'.format(\
            d=' '.join(map(str, d.products))))

    args = parser.parse_args()

    return args


if __name__ == '__main__':
    main()





