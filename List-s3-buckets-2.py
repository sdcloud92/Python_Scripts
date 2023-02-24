import json
import boto3
client = boto3.client('s3')

def lambda_handler(event, context):
    response = client.list_buckets()
    bucket = response['Buckets']
    
    print(bucket)
