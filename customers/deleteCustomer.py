import os
import boto3

if 'LOCALSTACK_HOSTNAME' in os.environ:
    dynamodb_endpoint = f"http://{os.environ['LOCALSTACK_HOSTNAME']}:4566"
    dynamodb = boto3.resource('dynamodb', endpoint_url=dynamodb_endpoint)
else:
    dynamodb = boto3.resource('dynamodb')
    
def deleteCustomer(event, context):
    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

    # delete the Customer from the database
    table.delete_item(
        Key={
            'id': event['pathParameters']['id']
        }
    )

    return {"statusCode": 200}