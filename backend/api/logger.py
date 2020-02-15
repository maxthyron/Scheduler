from termcolor import colored
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(message)s', datefmt='%H:%M:%S')
logging.getLogger("urllib3").setLevel(logging.WARNING)

class LogMachine:
    verbose = False

    @classmethod
    def info(cls, msg):
        if cls.verbose:
            logging.info(colored(msg, 'green'))

    @classmethod
    def error(cls, msg):
        if cls.verbose:
            logging.error(colored(msg, 'red'))

    @classmethod
    def attn(cls, msg):
        if cls.verbose:
            logging.debug(colored(msg, 'cyan'))
