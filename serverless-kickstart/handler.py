import logging

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


def cron(event, context):
    logger.debug("Event is: {}".format(event))
    logger.debug("Context is: {}".format(context))
