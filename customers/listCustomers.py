import json
import os
import boto3

if 'LOCALSTACK_HOSTNAME' in os.environ:
    dynamodb_endpoint = f"http://{os.environ['LOCALSTACK_HOSTNAME']}:4566"
    dynamodb = boto3.resource('dynamodb', endpoint_url=dynamodb_endpoint)
else:
    dynamodb = boto3.resource('dynamodb')

def listCustomers(event, context):
    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

    # fetch all Customers from the database
    result = table.scan()

    return {"statusCode": 200, "body": json.dumps(result['Items'])}