import boto3
from botocore.exceptions import ClientError
import json

s3_client = boto3.client('s3')


def lambda_handler(event, context):
    print('event:', json.dumps(event))
    bucket_name = event['pathParameters']['bucket']
    file_name = event['queryStringParameters']['file']
    response = s3_client.generate_presigned_post(
        Bucket=bucket_name,
        Key=file_name,
        Fields=None,
        Conditions=None,
        ExpiresIn=3600
    )
    url = {
        "url": response
    }

    return {
        "statusCode": 200,
        'headers': {
            'Content-Type': 'application/json'
        },
        'body': json.dumps(url)
    }