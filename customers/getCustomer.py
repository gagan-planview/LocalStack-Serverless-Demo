import os
import json
import boto3

if 'LOCALSTACK_HOSTNAME' in os.environ:
    dynamodb_endpoint = f"http://{os.environ['LOCALSTACK_HOSTNAME']}:4566"
    dynamodb = boto3.resource('dynamodb', endpoint_url=dynamodb_endpoint)
else:
    dynamodb = boto3.resource('dynamodb')


def getCustomer(event, context):
    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

    # fetch Customer from the database
    result = table.get_item(
        Key={
            'id': event['pathParameters']['id']
        }
    )

    return {"statusCode": 200, "body": json.dumps(result['Item'])}