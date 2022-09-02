import json
import logging
import os
import time
import uuid

import boto3
# from boto3 import client as boto3_client
from boto3 import session

if 'LOCALSTACK_HOSTNAME' in os.environ:
    dynamodb_endpoint = f"http://{os.environ['LOCALSTACK_HOSTNAME']}:4566"
    dynamodb = boto3.resource('dynamodb', endpoint_url=dynamodb_endpoint)
    ses_endpoint = f"http://{os.environ['LOCALSTACK_HOSTNAME']}:4566"
    ses_client = boto3.client("ses", region_name="us-west-2", endpoint_url=ses_endpoint)
else:
    dynamodb = boto3.resource('dynamodb')
    ses_client = boto3.client('ses')

def createCustomer(event, context):

    data = json.loads(event['body'])
    if 'firstName' not in data:
        logging.error("Validation Error")
        raise Exception("Couldn't create the Customer.")

    timestamp = str(time.time())

    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

    customer = {
        'id': str(uuid.uuid1()),
        'firstName': data['firstName'],
        'lastName': data['lastName'],
        'createdAt': timestamp,
        'updatedAt': timestamp,
    }

    # write the Customer to the database
    table.put_item(Item=customer)

    if 'email' not in data:
        logging.error("Validation Error")
        raise Exception("Email not found.")

    else:
        destinationEmail = data['email']
        response = ses_client.send_email(
            Source='hackathonSourceEmail@planview.com',
            Destination={
                'ToAddresses': [destinationEmail],
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

    return {"statusCode": 200, "body": json.dumps(customer)}