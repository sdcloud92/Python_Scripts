import boto3

# Set up the EC2 client
ec2 = boto3.client('ec2')

# Launch an EC2 instance
instance = ec2.run_instances(
    ImageId='ami-0123456789abcdef',
    InstanceType='t2.micro',
    MaxCount=1,
    MinCount=1
)

# Get the instance ID
instance_id = instance['Instances'][0]['InstanceId']
print('Launched instance with ID:', instance_id)
