import boto3
import uuid

def lambda_handler(event, context):
    # create an SQS resource object using Boto3
    sqs = boto3.resource('sqs')

    # define the name of your SQS queue
    queue_name = 'my-sqs-queue.fifo'

    # create an SQS FIFO queue with the given name
    queue = sqs.create_queue(QueueName=queue_name, Attributes={'FifoQueue': 'true'})

    # create a unique Message Group ID and Message Deduplication ID for the message
    message_group_id = 'my-message-group'
    message_deduplication_id = str(uuid.uuid4())

    # define the content of your message
    message_body = 'This is a test message.'

    # publish the message to your SQS queue
    queue.send_message(MessageBody=message_body, MessageGroupId=message_group_id, MessageDeduplicationId=message_deduplication_id)

    # return a success response with the name of the newly created queue
    return {
        'statusCode': 200,
        'body': f'Successfully created SQS FIFO queue {queue_name} and published a message with Message Deduplication ID {message_deduplication_id}'
    }
