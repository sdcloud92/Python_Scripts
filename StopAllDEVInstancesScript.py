import boto3

# create an EC2 client for the US East (Ohio) region
ec2_client = boto3.client('ec2', region_name='us-east-2')

# get a list of all running instances in the region
response = ec2_client.describe_instances(Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])

# stop all running instances with name that starts with "DEV"
stopped_instances = []
for reservation in response['Reservations']:
    for instance in reservation['Instances']:
        for tag in instance['Tags']:
            if tag['Key'] == 'Name' and tag['Value'].startswith('DEV'):
                ec2_client.stop_instances(InstanceIds=[instance['InstanceId']])
                stopped_instances.append(instance['InstanceId'])

# print confirmation message listing all the instances that were stopped or en error message
if stopped_instances:
    print("The following instances were successfully stopped:")
    for instance_id in stopped_instances:
        print(instance_id)
else:
    print("Error: No instances with name starting with 'DEV' were found running.")