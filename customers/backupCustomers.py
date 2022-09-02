import json
import os
import boto3
import tempfile

if 'LOCALSTACK_HOSTNAME' in os.environ:
    dynamodb_endpoint = f"http://{os.environ['LOCALSTACK_HOSTNAME']}:4566"
    dynamodb = boto3.resource('dynamodb', endpoint_url=dynamodb_endpoint)

    s3_endpoint= f"http://{os.environ['LOCALSTACK_HOSTNAME']}:4566"
    s3 = boto3.resource('s3', endpoint_url=s3_endpoint)
else:
    dynamodb = boto3.resource('dynamodb')
    s3 = boto3.resource('s3')

def backupCustomers(event, context):
    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

    # fetch all Customers from the database
    result = table.scan()

    result_body = json.dumps(result['Items'])
    print('result_body:',result_body)

    opt_file = tempfile.NamedTemporaryFile(mode="w+", encoding="utf-8", delete=False)
    opt_file.write(json.dumps(result_body))
    opt_file.flush()
    with open(opt_file.name, mode="r", encoding="utf-8") as reader:
        s3.Bucket(os.environ['S3_BUCKET']).put_object(Key="HACKATHON", Body=reader.read())
    opt_file.close()
    return {"statusCode": 200, "body": "Customer List BackedUp"}