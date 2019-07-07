from termcolor import colored
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(message)s', datefmt='%H:%M:%S')


class LogMachine:
    @staticmethod
    def info(msg):
        logging.info(colored(msg, 'green'))

    @staticmethod
    def error(msg):
        logging.error(colored(msg, 'red'))

    @staticmethod
    def attn(msg):
        logging.debug(colored(msg, 'cyan'))
