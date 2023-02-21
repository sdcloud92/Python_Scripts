import boto3
import os

# Define the lambda_handler function that will be triggered when the Lambda function is called
def lambda_handler(event, context):
    '''
    Extract the VPC ID from the event and enable VPC Flow Logs.
    '''
    try:
        # Extract the VPC ID from the event parameter
        vpc_id = event['detail']['responseElements']['vpc']['vpcId']

        # Print the VPC ID to the console
        print('VPC: ' + vpc_id)

        # Create a new EC2 client using the boto3 library
        ec2_client = boto3.client('ec2')

        # Describe the flow logs associated with the VPC using the describe_flow_logs method
        response = ec2_client.describe_flow_logs(
            Filter=[
                {
                    'Name': 'resource-id',
                    'Values': [
                        vpc_id,
                    ]
                },
            ],
        )

        # Check whether flow logs are already enabled for the VPC
        if len(response[u'FlowLogs']) != 0:
            # If flow logs are already enabled, print a message to the console
            print('VPC Flow Logs are ENABLED')
        else:
            # If flow logs are not enabled, print a message to the console and create flow logs
            print('VPC Flow Logs are DISABLED')

            # Print the names of the environment variables to the console
            print('FLOWLOGS_GROUP_NAME: ' + os.environ['FLOWLOGS_GROUP_NAME'])
            print('ROLE_ARN: ' + os.environ['ROLE_ARN'])

            # Create flow logs for the VPC using the create_flow_logs method
            response = ec2_client.create_flow_logs(
                ResourceIds=[vpc_id],
                ResourceType='VPC',
                TrafficType='ALL',
                LogGroupName=os.environ['FLOWLOGS_GROUP_NAME'],
                DeliverLogsPermissionArn=os.environ['ROLE_ARN'],
            )

            # Print the ID of the newly created flow logs to the console
            print('Created Flow Logs: ' + response['FlowLogIds'][0])

    # Catch any exceptions that may occur during the execution of the function
    except Exception as e:
        # Print an error message to the console with the reason for the exception
        print('Error - reason "%s"' % str(e))