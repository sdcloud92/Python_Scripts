import boto3
import datetime

def lambda_handler(event, context):
    ec2 = boto3.resource('ec2')
    instances = ec2.instances.filter(Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
    for instance in instances:
        launch_time = instance.launch_time
        elapsed_time = datetime.datetime.now(datetime.timezone.utc) - launch_time
        if elapsed_time > datetime.timedelta(minutes=30):
            instance.stop()
    return 'Success'