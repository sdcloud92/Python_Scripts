import json
import boto3
client = boto3.client('dynamodb')  

def lambda_handler(event, context):
    response = client.put_item(
        TableName='RetailSales24022023',
        Item={
            'customerID': {
                'S': '001',
            },
            'Product': {
                'S': 'mangoes',
            },
            'Quantity': {
                'N': '100',
            },
            'Address': {
                'S': '115 Queen Elizabeth Road',
            },
        },
    )
    
    print(response)