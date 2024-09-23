import logging
import sys
import datetime

logger = logging.getLogger()


# Get current time
def current_time():
    return datetime.datetime.now().isoformat()


logger.setLevel(logging.DEBUG)
LOG_FILE_PATH = "log/log_general_" + current_time().replace(":", "_") + ".log"

# Output to File
handlerF = logging.FileHandler(filename=LOG_FILE_PATH, encoding='utf-8', mode='w')
handlerF.setLevel(logging.INFO)
handlerF.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handlerF)

# Output to Console Screen
handlerC = logging.StreamHandler(sys.stdout)
handlerF.setLevel(logging.DEBUG)
handlerC.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handlerC)
