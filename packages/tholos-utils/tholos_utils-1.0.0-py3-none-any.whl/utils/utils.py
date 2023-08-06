import traceback
import logging

logger = logging.getLogger()
logger.setLevel(logging.ERROR)

def handle_error(err, status_code, message):
    logger.error(traceback.format_exc())
    logger.error(err)
    return {
        'statusCode': status_code,
        'body': message
    }