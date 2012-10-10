import logging

#The terminal has 8 colors with codes from 0 to 7
BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(8)

#These are the sequences need to get colored ouput
RESET_SEQ = "\033[0m"
COLOR_SEQ = "\033[1;%dm"
BOLD_SEQ =  "\033[1m"

#The background is set with 40 plus the number of the color,
#and the foreground with 30
COLORS = {
    'WARNING':  COLOR_SEQ % (30 + YELLOW) + 'WARNING' + RESET_SEQ,
    'INFO':     COLOR_SEQ % (30 + WHITE) + 'INFO' + RESET_SEQ,
    'DEBUG':    COLOR_SEQ % (30 + BLUE) + 'DEBUG' + RESET_SEQ,
    'CRITICAL': COLOR_SEQ % (30 + YELLOW) + 'CRITICAL' + RESET_SEQ,
    'ERROR':    COLOR_SEQ % (30 + RED) + 'ERROR' + RESET_SEQ,
}


class ColoredFormatter(logging.Formatter):
    def __init__(self, msg, use_color=True):
        logging.Formatter.__init__(self, msg)
        self.use_color = use_color

    def format(self, record):
        if self.use_color:
            record.levelname = COLORS.get(record.levelname, record.levelname)
        return logging.Formatter.format(self, record)


class WorkListLogger(logging.Logger):
    COLOR_FORMAT = "[" + BOLD_SEQ + "%(name)s" + RESET_SEQ + \
                   "][%(levelname)s] %(message)s (" + BOLD_SEQ + \
                   "%(filename)s" + RESET_SEQ + ":%(lineno)d)"
    NO_COLOR_FORMAT = "[%(name)s][%(levelname)s] %(message)s " \
                      "(%(filename)s:%(lineno)d)"
    LOG_FILE_HANDLER = None

    def __init__(self, name):
        logging.Logger.__init__(self, name)

        #Add two handlers, a stderr one, and a file one
        color_formatter = ColoredFormatter(WorkListLogger.COLOR_FORMAT)
        #no_color_formatter = ColoredFormatter(WorkListLogger.NO_COLOR_FORMAT,False)

        #create the single file appending handler
        #if WorkListLogger.LOG_FILE_HANDLER == None:
        #    filename = os.path.join(CONFIG_ROOT, 'ubuntu-tweak.log')
        #    WorkListLogger.LOG_FILE_HANDLER = logging.FileHandler(filename, 'w')
        #    WorkListLogger.LOG_FILE_HANDLER.setFormatter(no_color_formatter)

        console = logging.StreamHandler()
        console.setFormatter(color_formatter)

        #self.addHandler(WorkListLogger.LOG_FILE_HANDLER)
        self.addHandler(console)
        print 'addHandler'
        return


def enable_debugging():
    logging.getLogger().setLevel(logging.DEBUG)


def disable_debugging():
    logging.getLogger().setLevel(logging.INFO)


def disable_logging():
    logging.getLogger().setLevel(logging.CRITICAL + 1)

#logging.setLoggerClass(WorkListLogger)

def log_func(log):
    def wrap(func):
        def func_wrapper(*args, **kwargs):
            log.addHandler(logging.StreamHandler())
            log.debug("%s:" % func)
            for i, arg in enumerate(args):
                log.debug("\targs-%d: %s" % (i + 1, arg))
            for k, v in enumerate(kwargs):
                log.debug("\tdict args-%d: %s: %s" % (k, v, kwargs[v]))
            return func(*args, **kwargs)
        return func_wrapper
    return wrap
