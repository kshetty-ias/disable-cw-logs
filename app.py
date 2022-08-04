import json
import logging
from logging import basicConfig

import boto3
from botocore.exceptions import ClientError
from flask import Flask, jsonify

app = Flask(__name__)

region_name = "us-east-1"
session = boto3.session.Session()

secret_name="dev/disable-logs"

def get_secret(secret_name):
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        response = client.get_secret_value(SecretId=secret_name)
    except ClientError as e:
        raise e
    else:
        return json.loads(response['SecretString']).get('CW_LOGS')

def update_secret(flag):
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    new_secret_string = '{"CW_LOGS":"1"}' if flag == True else '{"CW_LOGS":"0"}'

    try:
        client.put_secret_value(
            SecretId=secret_name, 
            SecretString=new_secret_string
        )
    except ClientError as e:
        raise e

LOGGING = True if get_secret(secret_name) == "1" else False

@app.route('/logs/<flag>', methods=['POST'])
def toggle_logs(flag):
    out = {}
    flag = bool(int(flag))

    secret = True if get_secret(secret_name) == "1" else False

    if (flag == secret == False):
        out['error'] = 'Logs are already disabled'
        return jsonify(out), 400
    elif (flag == secret == True):
        out['error'] = 'Logs are already enabled'
        return jsonify(out), 400
    else:
        try:
            update_secret(flag)
        except ClientError as e:
            out['error'] = e.response['Error']['Code']
        else:
            out['message'] = 'Logs enabled' if flag == True else 'Logs disabled'
    
    return jsonify(out)


logger = logging.getLogger(__name__)

if (LOGGING == True):
    logger.disabled = False
    logger.handlers.clear()
    basicConfig(filename='example.log', filemode='w', encoding='utf-8', level=logging.DEBUG)

    logger.warning('Show this warning!!')
else:
    logger.disabled = True
    logger.propagate = False

    logger.warning('Do not show this!!')


if __name__ == '__main__':
    app.run(debug=True)

