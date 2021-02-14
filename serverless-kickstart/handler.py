import boto3
import os
import logging

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

API_KEY_NAME = os.environ.get("API_KEY_NAME", "api_key")

boto_session = boto3.session.Session()
secrets_manager = boto_session.client("secretsmanager")
API_KEY = secrets_manager.get_secret_value(SecretId=API_KEY_NAME)["SecretString"]


def cron(event, context):
    logger.debug("Event is: {}".format(event))
    logger.debug("Context is: {}".format(context))
    logger.debug("API Key name is: {}".format(API_KEY_NAME))
    logger.debug("API Key is: {}".format(API_KEY))
