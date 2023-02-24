import json
import boto3
client = boto3.client('s3')

def lambda_handler(event, context):
    response = client.delete_bucket(
    Bucket='lambdapythoncreatebucket24022023',
)

    print(response)

