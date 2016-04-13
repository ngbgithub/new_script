'''The purpose of this module is to provide the installation prefix so
that one can e.g. infer the location of config files.
'''

import logging
logger = logging.getLogger(__name__.split('.')[-1])
logger.addHandler(logging.NullHandler())


def prefix():
    ''':returns: The installation prefix.
    :rtype: :class:`str`
    '''
    try:
        from . import local_conf
        return local_conf.prefix
    except ImportError:
        import os.path
        # If _conf.py doesn't exist, assume we're working in the
        #   source directory.
        thisDir = os.path.dirname(__file__)
        return os.path.abspath(os.path.join(thisDir, '..', '..'))


