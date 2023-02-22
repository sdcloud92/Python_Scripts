import boto3

def lambda_handler(event, context):
    # create an SQS resource object using Boto3
    sqs = boto3.resource('sqs')

    # define the name of your SQS queue
    queue_name = 'my-sqs-queue'

    # create an SQS queue with the given name
    queue = sqs.create_queue(QueueName=queue_name)

    # return a success response with the name of the newly created queue
    return {
        'statusCode': 200,
        'body': f'Successfully created SQS queue {queue_name}'
    }