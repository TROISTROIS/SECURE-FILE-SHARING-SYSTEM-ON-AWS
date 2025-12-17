import logging
import os
import boto3
from botocore.exceptions import ClientError
import json

# Remove profile_name for Lambda deployment - use IAM role instead
session = boto3.Session()
s3_client = session.client('s3')


def create_bucket(bucket_name):
    try:
        response = s3_client.create_bucket(Bucket=bucket_name)
        return {
            'status': 'success',
            'message': 'Bucket created successfully',
            'response': str(response)
        }
    except Exception as e:
        return {
            'status': 'error',
            'message': f'Failed to create S3 bucket: {str(e)}'
        }


def create_presigned_post(bucket_name, object_name):
    """Generate presigned upload URL"""
    try:
        response = s3_client.generate_presigned_post(
            Bucket=bucket_name,  # Fixed parameter name
            Key=object_name,  # Fixed: object_name → Key
            ExpiresIn=3600
        )
        return {
            'status': 'success',
            'presigned_post_url': response
        }
    except ClientError as e:
        return {
            'status': 'error',
            'message': f'Failed to generate UPLOAD URL: {str(e)}'
        }


def create_presigned_url(bucket_name, object_name):
    """Generate presigned download URL"""
    try:
        response = s3_client.generate_presigned_url(
            'get_object',
            Params={
                'Bucket': bucket_name,
                'Key': object_name
            },
            ExpiresIn=3600
        )
        return {
            'status': 'success',
            'presigned_get_url': response
        }
    except ClientError as e:
        return {
            'status': 'error',
            'message': f'Failed to generate DOWNLOAD URL: {str(e)}'
        }


def lambda_handler(event, context):
    # Get parameters from event
    action = event.get('action', 'create_bucket')  # Default action
    bucket_name = event.get('bucket_name', 'secure-file-sharing-s3-bucket-fn')
    object_name = event.get('object_name', 'picture.jpg')

    # Route to appropriate function based on action
    if action == 'create_bucket':
        result = create_bucket(bucket_name)
    elif action == 'upload':
        result = create_presigned_post(bucket_name, object_name)
    elif action == 'download':
        result = create_presigned_url(bucket_name, object_name)
    else:
        result = {
            'status': 'error',
            'message': 'Invalid action. Use: create_bucket, upload, or download'
        }

    # Return Lambda response format
    status_code = 200 if result['status'] == 'success' else 400
    return {
        'statusCode': status_code,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps(result)
    }
