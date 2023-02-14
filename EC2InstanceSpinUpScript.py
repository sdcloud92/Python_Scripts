import boto3


# create a boto3 resource for EC2 in the US East (Ohio) region
ec2 = boto3.resource('ec2', region_name='us-east-2')

# create PROD instances
# create a single instance with Amazon Linux AMI, t2.micro instance type, and assign the Name and Type tags
# for PROD1 instance
prod1 = ec2.create_instances(
    ImageId='ami-0c55b159cbfafe1f0', 
    InstanceType='t2.micro', 
    MinCount=1, 
    MaxCount=1,
    TagSpecifications=[
        {
            'ResourceType': 'instance',
            'Tags': [
                {
                    'Key': 'Name',
                    'Value': 'PROD1'
                },
                {
                    'Key': 'Type',
                    'Value': 'PROD'
                }
            ]
        }
    ]
)
# for PROD2 instance
prod2 = ec2.create_instances(
    ImageId='ami-0c55b159cbfafe1f0', 
    InstanceType='t2.micro', 
    MinCount=1, 
    MaxCount=1,
    TagSpecifications=[
        {
            'ResourceType': 'instance',
            'Tags': [
                {
                    'Key': 'Name',
                    'Value': 'PROD2'
                },
                {
                    'Key': 'Type',
                    'Value': 'PROD'
                }
            ]
        }
    ]
)

# create DEV instances
# create a single instance with Amazon Linux AMI, t2.micro instance type, and assign the Name and Type tags
# for DEV1 instance
dev1 = ec2.create_instances(
    ImageId='ami-0c55b159cbfafe1f0', 
    InstanceType='t2.micro', 
    MinCount=1, 
    MaxCount=1,
    TagSpecifications=[
        {
            'ResourceType': 'instance',
            'Tags': [
                {
                    'Key': 'Name',
                    'Value': 'DEV1'
                },
                {
                    'Key': 'Type',
                    'Value': 'DEV'
                }
            ]
        }
    ]
)
# for DEV2 instance
dev2 = ec2.create_instances(
    ImageId='ami-0c55b159cbfafe1f0', 
    InstanceType='t2.micro', 
    MinCount=1, 
    MaxCount=1,
    TagSpecifications=[
        {
            'ResourceType': 'instance',
            'Tags': [
                {
                    'Key': 'Name',
                    'Value': 'DEV2'
                },
                {
                    'Key': 'Type',
                    'Value': 'DEV'
                }
            ]
        }
    ]
)

# create TESTING instances
# create a single instance with Amazon Linux AMI, t2.micro instance type, and assign the Name and Type tags
# for TESTING1 instance
testing1 = ec2.create_instances(
    ImageId='ami-0c55b159cbfafe1f0', 
    InstanceType='t2.micro', 
    MinCount=1, 
    MaxCount=1,
    TagSpecifications=[
        {
            'ResourceType': 'instance',
            'Tags': [
                {
                    'Key': 'Name',
                    'Value': 'TESTING1'
                },
                {
                    'Key': 'Type',
                    'Value': 'TESTING'
                }
            ]
        }
    ]
)
# for TESTING2 instance
testing2 = ec2.create_instances(
    ImageId='ami-0c55b159cbfafe1f0', 
    InstanceType='t2.micro', 
    MinCount=1, 
    MaxCount=1,
    TagSpecifications=[
        {
            'ResourceType': 'instance',
            'Tags': [
                {
                    'Key': 'Name',
                    'Value': 'TESTING2'
                },
                {
                    'Key': 'Type',
                    'Value' : 'Name'
                }
            ]
        }
    ]
)
# print confirmation of created instances
for instance in [prod1[0], prod2[0], dev1[0], dev2[0], testing1[0], testing2[0]]:
    print("Instance Successfully created: ", instance.id)