import json
import boto3
client = boto3.client('s3')

def lambda_handler(event, context):
    response = client.create_bucket(
    Bucket='democreatebucket24022023',
    CreateBucketConfiguration={
        'LocationConstraint': 'us-east-2' # Cannot use -use-east-1 in Lambda
    },
    
)
