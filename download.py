import json
import boto3

def lambda_handler(event,context):
    print('event:', json.dumps(event))
    s3_client = boto3.client('s3')
    bucket_name = event['pathParameters']['bucket']
    file_name=event['queryStringParameters']['file']
    print(bucket_name,file_name)
    URL = s3_client.generate_presigned_url(
        'get_object',
        Params={'Bucket': bucket_name,
        'Key': file_name}, ExpiresIn=3600)
    print(bucket_name, file_name)
    url = {
        "URL": URL
    }

    return {
        "statusCode":200,
        'headers':{
            'Content-Type':'application/json'
        },
        'body': json.dumps(url)
    }