import logging, os.path
logger = logging.getLogger(__name__.split('.')[-1])
logger.addHandler(logging.NullHandler())

loggerIsInitialized = False


def configureLogger(confFilename):
    '''Read the logging.conf config file, and set up the logger
    appropriately.
    '''
    import date_file_handler
    import logging.config

    # Check that the appropriate filename exists.
    if not os.path.isfile(confFilename):
        raise Exception('File not found: {}'.format(confFilename))

    # This hack lets us specify our own custom handler inside the
    #   logging config file.
    logging.DateFileHandler = date_file_handler.DateFileHandler

    confDir = os.path.dirname(confFilename)
    prefixDir = os.path.abspath(os.path.join(confDir, '..', '..'))
    # We temporarily change the current working directory so that the
    #   log file can be specified as a relative path.
    orig = os.getcwd()
    try:
        os.chdir(prefixDir)
        # Load the config file.
        logging.config.fileConfig(confFilename, disable_existing_loggers=False)

    finally:
        os.chdir(orig)

    global loggerIsInitialized
    loggerIsInitialized = True


def logArgs(args):
    '''Print a summary of the command line arguments to the logger.
    '''
    import inspect
    bannerWidth = 30
    logger.info('Command line settings'.center(bannerWidth, '='))
    members = inspect.getmembers(args)
    for member in members:
        name, val = member[0], member[1]
        if len(name) > 1 and name[0:2] == '__':
            continue
        if hasattr(val, '__call__'):
            continue
        logger.info('{}: {}'.format(name.rjust(16), val))
    logger.info(''.rjust(bannerWidth, '='))


def manageException(e, emitTrace):
    '''Print out an error message from an exception in different
    possible ways, depending on whether the user wants a stack trace,
    and whether the logger is enabled.
    '''
    msg = '{}'.format(e)
    if not loggerIsInitialized:
        if emitTrace:
            raise
        else:
            print('ERROR: ', msg)
    else: # The logger has been initialized.
        if emitTrace:
            logger.exception(msg)
        else:
            logger.error(msg)


