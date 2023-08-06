import traceback
import logging
import os
import boto3
from botocore.exceptions import ClientError
import json
import psycopg2

logger = logging.getLogger()
logger.setLevel(logging.ERROR)

def handle_api_error(err, status_code, message):
    logger.error(traceback.format_exc())
    logger.error(err)
    return {
        'statusCode': status_code,
        'body': message
    }

def get_secret_json(secret_name,access_key,secret_key,region):
    session = boto3.session.Session(
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        region_name=region
    )

    client = session.client(
        service_name='secretsmanager',
        region_name=region
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        # For a list of exceptions thrown, see
        # https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
        raise e

    # Decrypts secret using the associated KMS key.
    secret = get_secret_value_response['SecretString']
    return json.loads(secret)

def close_connection(cursor, db):
    cursor.close()
    db.close()

def get_db(db_secret_name,access_key_name,secret_key_name,region):
    db_secrets = get_secret_json(db_secret_name,access_key_name,secret_key_name,region)
    db = psycopg2.connect(
        host=db_secrets['host'],
        user=db_secrets['username'],
        password=db_secrets['password'],
        database=db_secrets['database']
    )
    db.autocommit = True
    return db