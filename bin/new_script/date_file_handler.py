import datetime, logging


class DateFileHandler(logging.FileHandler):
    def __init__(self, filename, mode):
        now = datetime.datetime.now()
        filename = now.strftime(filename)
        logging.FileHandler.__init__(self, filename, mode)
