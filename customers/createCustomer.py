import json
import logging
import os
import time
import uuid

import boto3

if 'LOCALSTACK_HOSTNAME' in os.environ:
    dynamodb_endpoint = f"http://{os.environ['LOCALSTACK_HOSTNAME']}:4566"
    dynamodb = boto3.resource('dynamodb', endpoint_url=dynamodb_endpoint)
else:
    dynamodb = boto3.resource('dynamodb')


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

    return {"statusCode": 200, "body": json.dumps(customer)}