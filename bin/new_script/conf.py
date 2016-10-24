'''The purpose of this module is to provide the installation prefix so
that one can e.g. infer the location of config files.
'''

import logging
logger = logging.getLogger(__name__.split('.')[-1])
logger.addHandler(logging.NullHandler())


def _prefix():
    ''':returns: The installation prefix.
    :rtype: :class:`str`
    '''
    try:
        from . import local_conf
        p = local_conf.prefix
    except ImportError:
        import os.path
        # If _conf.py doesn't exist, assume we're working in the
        #   source directory.
        thisDir = os.path.dirname(__file__)
        p = os.path.abspath(os.path.join(thisDir, '..', '..'))
    return p


def _version():
    '''The current version of the packages, as reflected by the VERSION file.
    '''
    try:
        from . import local_conf
        v = local_conf.version
    except ImportError:
        import os.path
        filename = os.path.join(prefix, 'VERSION')
        with open(filename, 'r') as fin:
            v = fin.read().strip()
    return v


prefix=_prefix()
version=_version()

