import boto3
import os
import logging
import requests
import gspread
import json
from google.oauth2.service_account import Credentials

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# aws services
boto_session = boto3.session.Session()
secrets_manager = boto_session.client("secretsmanager")

# variables
API_KEY_NAME = os.environ.get("API_KEY_NAME", "api_key")
API_KEY = secrets_manager.get_secret_value(SecretId=API_KEY_NAME)["SecretString"]
QUERY = 'port:17 product:"Windows qotd"'
url = f"https://api.shodan.io/shodan/host/search?key={API_KEY}&query={QUERY}"

DEFAULT_SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]
SERVICE_ACCOUNT_SECRET_NAME = os.environ.get("SERVICE_ACCOUNT_SECRET_NAME", "")
service_json = secrets_manager.get_secret_value(SecretId=SERVICE_ACCOUNT_SECRET_NAME)[
    "SecretString"
]
service_dict = json.loads(service_json)
credentials = Credentials.from_service_account_info(
    info=service_dict, scopes=DEFAULT_SCOPES
)
gc = gspread.authorize(credentials)


def cron(event, context):
    logger.debug("Event is: {}".format(event))
    logger.debug("Context is: {}".format(context))
    logger.debug("API Key name is: {}".format(API_KEY_NAME))

    shodan_results = []
    result_count = 0
    result = requests.get(url)
    if result.status_code == 200:
        shodan_results = result.json()["matches"]
        result_count = result.json()["total"]
        for result in shodan_results[:5]:
            logger.info(f"{result['location']['country_name']} says {result['data']}")
    logger.info(f"retrieved {len(shodan_results)} out of {result_count} total results ")

    sh = gc.open("shodan output")
    worksheet = sh.sheet1
    for i, result in enumerate(shodan_results[:5], start=1):
        worksheet.update_cell(
            i, 1, f"{result['location']['country_name']} says {result['data']}"
        )
