import json
import logging
from logging.config import dictConfig
import os
from random import random
import subprocess
from time import sleep
from threading import Thread
from flask import Flask, jsonify

CW_LOGS = bool(int(os.environ.get('CW_LOGS', 0)))


def update_cw_logs(logger):
    global CW_LOGS

    prev = CW_LOGS
    print(f'Old: {CW_LOGS}')
    subprocess.run(['cd', '..'])
    CW_LOGS = subprocess.check_output(['sh', 'scripts/app.sh'])
    CW_LOGS = bool(int(CW_LOGS.decode('UTF-8')))
    print(f'New: {CW_LOGS}\n')

    if (prev != CW_LOGS):
        toggle_logs(logger)


def periodic_fn(logger):
    while True:
        sleep(3)
        update_cw_logs(logger)
        print('Periodic function')


def start(app):

    @app.route('/hello', methods=['GET'])
    def hello_there():
        return jsonify({'data': 'Hello There'})
    
    app.run(port=5000)


def toggle_logs(logger):
    if (CW_LOGS == True):
        logger.disabled = False
        logger.handlers.clear()
        logger.propagate = False

        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        logger.addHandler(ch)

        logger.debug('debug message')
        logger.info('info message')
        logger.warning('warn message')
        logger.error('error message')
        logger.critical('critical message')
    else:
        logger.disabled = True
        logger.propagate = False

        logger.debug('!!!debug message')
        logger.info('!!!info message')
        logger.warning('!!!warn message')
        logger.error('!!!error message')
        logger.critical('!!!critical message')


def main():
    app = Flask(__name__)

    # Configure logging
    logger = logging.getLogger(__name__)
    print('Starting background task...')
    daemon = Thread(target=periodic_fn, daemon=True,
                    name='CW_Logs', args=(logger,))
    daemon.start()
    toggle_logs(logger)

    start(app)

    return app

if __name__ == "__main__":
    main()
