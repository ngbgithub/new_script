#!/usr/bin/env python

''''Do X.
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
            self.products = [4107]
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


def sampleQuery(cursor, productTypes):
    '''Do X.
    '''
    query = '''
        select
            h.account_number,
            cast(h.gl_balance as number(26, 2)) as gl_balance
        from
            bdr_core.liability_account_history h
        where
            h.account_status != 4
            and h.product_type in ({products})
            -- and rownum < 11 -- debug
    '''

    # We have to do this because there's no way to use ? arguments
    #   with variable numbers of arguments.
    if not [type(p)==int for p in productTypes]:
        # Be positive we can't have SQL injections.
        raise Exception('Product types must be integers') 
    query = query.format(products=', '.join(map(str, productTypes)))

    cursor.execute(query)

    logger.info('Getting first batch of rows...')
    row = cursor.fetchone()
    c = 0

    accounts = {}
    logger.info('Getting additional rows...')
    while row is not None:
        c += 1



        row = cursor.fetchone()
    logger.info('{} rows retrieved.'.format(c))


if __name__ == '__main__':
    main()





