import json
import logging
from logging.config import dictConfig
import os
import subprocess
from time import sleep

CW_LOGS = bool(int(os.environ.get('CW_LOGS', 1)))

def update_cw_logs():
    global CW_LOGS

    prev = CW_LOGS
    print(f'Old: {CW_LOGS}')  
    CW_LOGS = subprocess.check_output(['sh', '../scripts/app.sh'])
    CW_LOGS = bool(int(CW_LOGS.decode('UTF-8')))
    print(f'New: {CW_LOGS}\n')

    if (prev != CW_LOGS):
        toggle_logs()

def periodic_fn():
    while True:
        sleep(3)
        update_cw_logs()

logger = logging.getLogger(__name__)

def toggle_logs():
    if (CW_LOGS == True):
        logger.disabled = False
        logger.handlers.clear()
        logger.propagate = False

        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
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

toggle_logs()
periodic_fn()