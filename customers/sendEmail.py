import json
import logging
import os
import time
import uuid
import boto3


if 'LOCALSTACK_HOSTNAME' in os.environ:
    ses_endpoint = f"http://{os.environ['LOCALSTACK_HOSTNAME']}:4566"
    ses_client = boto3.client("ses", region_name="us-west-2", endpoint_url=ses_endpoint)
else:
    ses_client = boto3.client('ses')
CHARSET = "UTF-8"

def sendEmail(event, context):

    response = ses_client.send_email(
        Source='hackathonSourceEmail@planview.com',
        Destination={
            'ToAddresses': ['hackathonDestinatiomEmail@planview.com'],
        },
        ReplyToAddresses=['hackathonSourceEmail@planview.com'],
        Message={
            'Subject': {
                'Data': 'New customer created',
                'Charset': 'utf-8'
            },
            'Body': {
                'Text': {
                    'Data': 'New customer created',
                    'Charset': 'utf-8'
                },
                'Html': {
                    'Data': 'New customer created',
                    'Charset': 'utf-8'
                }
            }
        }
    )
    return {"statusCode": 200, "body": 'New customer created in Localstack'}