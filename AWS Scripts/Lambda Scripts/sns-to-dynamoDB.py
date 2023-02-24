import json
import boto3
import time
import uuid

dynamodb = boto3.client('dynamodb')
sns = boto3.client('sns')

def lambda_handler(event, context):
    message = event['Records'][0]['Sns']['Message']
    topic_arn = event['Records'][0]['Sns']['TopicArn']
    timestamp = str(time.time())
    identifier = str(uuid.uuid4())
    
    # Check if the DynamoDB table exists
    table_name = 'order_records'
    try:
        table = dynamodb.describe_table(TableName=table_name)
    except dynamodb.exceptions.ResourceNotFoundException:
        # Create the table if it doesn't exist
        table = dynamodb.create_table(
            TableName=table_name,
            KeySchema=[
                {
                    'AttributeName': 'identifier',
                    'KeyType': 'HASH'
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'identifier',
                    'AttributeType': 'S'
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )
        # Wait for the table to be created
        dynamodb.get_waiter('table_exists').wait(TableName=table_name)
    
    # Extract relevant information from the message
    relevant_info = json.loads(message)
    # Store relevant information in DynamoDB
    dynamodb.put_item(
        TableName=table_name,
        Item={
            'topic_arn': {'S': topic_arn},
            'timestamp': {'N': timestamp},
            'identifier': {'S': identifier},
            'relevant_info': {'S': json.dumps(relevant_info)}
        }
    )
    
    # Call another Lambda function
    response = sns.publish(
        TargetArn='arn:aws:sns:us-east-2:126808424343:Orders',
        Message=json.dumps({'timestamp': timestamp, 'identifier': identifier})
    )
    
    return {
        'statusCode': 200,
        'body': json.dumps('Order information log stored in company records.')
    }