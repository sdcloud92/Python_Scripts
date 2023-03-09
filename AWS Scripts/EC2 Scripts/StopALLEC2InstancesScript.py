import boto3

# create an EC2 client for the US East (Ohio) region
ec2_client = boto3.client('ec2', region_name='us-east-2')

# get a list of all running instances in the region
response = ec2_client.describe_instances(Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])

# stop all running instances in the region
stopped_instances = []
for reservation in response['Reservations']:
    for instance in reservation['Instances']:
        response = ec2_client.stop_instances(InstanceIds=[instance['InstanceId']])
        stopped_instances.extend(response['StoppingInstances'])

# print confirmation message
stopped_instance_ids = [instance['InstanceId'] for instance in stopped_instances]
if stopped_instance_ids:
    print("The following instances were successfully stopped:")
    for instance_id in stopped_instance_ids:
        print(instance_id)
else:
    print("No instances were found running.")