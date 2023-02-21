import boto3
import base64
import os
import uuid
import time

# Set up the Boto3 EC2, RDS, Auto Scaling, and Elastic Load Balancing V2 clients
ec2 = boto3.client('ec2')
rds = boto3.client('rds')
elbv2 = boto3.client('elbv2')
autoscaling = boto3.client('autoscaling')

# Create the VPC with a CIDR block of 10.10.0.0/16
vpc_response = ec2.create_vpc(CidrBlock='10.10.0.0/16')
vpc_id = vpc_response['Vpc']['VpcId']
print(f"Created VPC with ID {vpc_id}")

# Create the two public subnets in two different availability zones
subnet_response1 = ec2.create_subnet(VpcId=vpc_id, CidrBlock='10.10.1.0/24', AvailabilityZone='us-east-2a')
subnet_response2 = ec2.create_subnet(VpcId=vpc_id, CidrBlock='10.10.2.0/24', AvailabilityZone='us-east-2b')
subnet_id1 = subnet_response1['Subnet']['SubnetId']
subnet_id2 = subnet_response2['Subnet']['SubnetId']
print(f"Created public subnets with IDs {subnet_id1} and {subnet_id2}")

# Create the four private subnets in two different availability zones
subnet_response3 = ec2.create_subnet(VpcId=vpc_id, CidrBlock='10.10.3.0/24', AvailabilityZone='us-east-2a')
subnet_response4 = ec2.create_subnet(VpcId=vpc_id, CidrBlock='10.10.4.0/24', AvailabilityZone='us-east-2b')
subnet_response5 = ec2.create_subnet(VpcId=vpc_id, CidrBlock='10.10.5.0/24', AvailabilityZone='us-east-2a')
subnet_response6 = ec2.create_subnet(VpcId=vpc_id, CidrBlock='10.10.6.0/24', AvailabilityZone='us-east-2b')
subnet_id3 = subnet_response3['Subnet']['SubnetId']
subnet_id4 = subnet_response4['Subnet']['SubnetId']
subnet_id5 = subnet_response5['Subnet']['SubnetId']
subnet_id6 = subnet_response6['Subnet']['SubnetId']
print(f"Created private subnets with IDs {subnet_id3} and {subnet_id4} and {subnet_id5} and {subnet_id6}")

# Create the internet gateway and attach it to the VPC
igw_response = ec2.create_internet_gateway()
igw_id = igw_response['InternetGateway']['InternetGatewayId']
ec2.attach_internet_gateway(InternetGatewayId=igw_id, VpcId=vpc_id)
print(f"Created internet gateway with ID {igw_id}")

# Create the public route table and add a route to the internet gateway
rt_response = ec2.create_route_table(VpcId=vpc_id)
rt_id = rt_response['RouteTable']['RouteTableId']
ec2.create_route(RouteTableId=rt_id, DestinationCidrBlock='0.0.0.0/0', GatewayId=igw_id)
ec2.associate_route_table(RouteTableId=rt_id, SubnetId=subnet_id1)
ec2.associate_route_table(RouteTableId=rt_id, SubnetId=subnet_id2)
print(f"Created public route table with ID {rt_id}")

# Create the private route table
rt_response = ec2.create_route_table(VpcId=vpc_id)
rt_id2 = rt_response['RouteTable']['RouteTableId']
ec2.associate_route_table(RouteTableId=rt_id2, SubnetId=subnet_id3)
ec2.associate_route_table(RouteTableId=rt_id2, SubnetId=subnet_id4)
print(f"Created private route table with ID {rt_id2}")

# Create the security group for the web tier
sg_response = ec2.create_security_group(GroupName='WebTierSG', Description='Security group for the Web tier', VpcId=vpc_id)
web_sg_id = sg_response['GroupId']
ec2.authorize_security_group_ingress(GroupId=web_sg_id, IpPermissions=[
{'IpProtocol': 'tcp', 'FromPort': 443, 'ToPort': 443, 'IpRanges': [{'CidrIp': '0.0.0.0/0'}]},
{'IpProtocol': 'tcp', 'FromPort': 20, 'ToPort': 20, 'IpRanges': [{'CidrIp': '0.0.0.0/0'}]}])
print(f"Created security group for the Web tier with ID {web_sg_id}")

# Create the security group for the application tier
sg_response = ec2.create_security_group(GroupName='AppTierSG', Description='Security group for the Application tier', VpcId=vpc_id)
app_sg_id = sg_response['GroupId']
ec2.authorize_security_group_ingress(GroupId=app_sg_id, IpPermissions=[{'IpProtocol': 'tcp', 'FromPort': 80, 'ToPort': 80, 'UserIdGroupPairs': [{'GroupId': web_sg_id}]}])
print(f"Created security group for the Application tier with ID {app_sg_id}")

# Create the security group for the RDS database tier
sg_response = ec2.create_security_group(GroupName='DBSG', Description='Security group for the Database tier', VpcId=vpc_id)
db_sg_id = sg_response['GroupId']
ec2.authorize_security_group_ingress(GroupId=db_sg_id, IpPermissions=[{'IpProtocol': 'tcp', 'FromPort': 3306, 'ToPort': 3306, 'UserIdGroupPairs': [{'GroupId': app_sg_id}]}])
print(f"Created security group for the Database tier with ID {db_sg_id}")

#Create the load balancer for the Web Tier
lb_response = elbv2.create_load_balancer(
    Name='WebTierLB',
    Subnets=[subnet_id1, subnet_id2],
    SecurityGroups=[web_sg_id],
    Scheme='internet-facing',
    Type='application'
)
lb_arn = lb_response['LoadBalancers'][0]['LoadBalancerArn']
print(f"Created load balancer for the Web tier with ARN {lb_arn}")

# Create the target group for the Web Tier
tg_response = elbv2.create_target_group(
    Name='WebTierTG',
    Protocol='HTTP',
    Port=80,
    TargetType='instance',
    VpcId=vpc_id
)
tg_arn = tg_response['TargetGroups'][0]['TargetGroupArn']
print(f"Created target group for the Web tier with ARN {tg_arn}")

# Generate a random name for the key pair
key_name = f"my_keypair_{uuid.uuid4()}"

# Create a new key pair
key_pair_response = ec2.create_key_pair(KeyName=key_name)
private_key = key_pair_response['KeyMaterial']

# Save the private key to a file
key_file_name = f"{key_name}.pem"
with open(key_file_name, 'x') as f:
    f.write(private_key)
os.chmod(key_file_name, 0o400)

print(f"Created new key pair with name {key_name} and saved private key to {key_file_name}")

# Create the launch template for the Web tier instances
user_data = '#!/bin/bash\necho "Hello, World!" > /var/www/html/index.html'
encoded_user_data = base64.b64encode(user_data.encode('utf-8')).decode('utf-8')
lt_response = ec2.create_launch_template(
    LaunchTemplateName='WebTierTemplate',
    LaunchTemplateData={
        'ImageId': 'ami-0c55b159cbfafe1f0',
        'InstanceType': 't2.micro',
        'KeyName': key_name, # Use the variable value
        'SecurityGroupIds': [web_sg_id],
        'UserData': encoded_user_data
    }
)
lt_id = lt_response['LaunchTemplate']['LaunchTemplateId']
print(f"Created launch template for the Web tier with ID {lt_id}")

# Generate a random name for the Auto Scaling group
asg_name = f"WebTierASG_{uuid.uuid4()}"

try:
    # Create an ASG for Web tier instances with the target group
    web_asg_response = autoscaling.create_auto_scaling_group(
        AutoScalingGroupName=asg_name,
        LaunchTemplate={
            'LaunchTemplateName': 'WebTierTemplate',
            'Version': '$Latest'
        },
        MinSize=3,
        MaxSize=10,
        TargetGroupARNs=[tg_arn],
        VPCZoneIdentifier=f"{subnet_id1},{subnet_id2}"
    )
    web_asg_name = web_asg_response['AutoScalingGroupName']
    print(f"Created auto scaling group for the Web tier with name {web_asg_name}")
except Exception as e:
    print(f"An error occurred while creating the Auto Scaling group: {e}")
    # Print additional debugging information
    print(f"tg_arn: {tg_arn}")
    print(f"subnet_id1: {subnet_id1}")
    print(f"subnet_id2: {subnet_id2}")
    asg_describe_response = autoscaling.describe_auto_scaling_groups()
    print(asg_describe_response)
    lt_describe_response = ec2.describe_launch_templates()
    print(lt_describe_response)

# Generate a new key pair with a random name
key_name = f"my_keypair_{uuid.uuid4()}"
key_pair_response = ec2.create_key_pair(KeyName=key_name)
private_key = key_pair_response['KeyMaterial']

# Save the private key to a file
key_file_name = f"{key_name}.pem"
with open(key_file_name, 'x') as f:
    f.write(private_key)
os.chmod(key_file_name, 0o400)

print(f"Created new key pair with name {key_name} and saved private key to {key_file_name}")

# Create the launch template for the application tier instances
user_data = '''#!/bin/bash
echo "Hello, World!" > /var/www/html/index.html
'''
encoded_user_data = base64.b64encode(user_data.encode('utf-8')).decode('utf-8')
lt_response = ec2.create_launch_template(
    LaunchTemplateName='AppTierTemplate',
    LaunchTemplateData={
        'ImageId': 'ami-0c55b159cbfafe1f0', # Choose your own AMI ID
        'InstanceType': 't2.micro',
        'KeyName': key_name, # Use the newly created key pair name
        'SecurityGroupIds': [app_sg_id],
        'UserData': encoded_user_data
    }
)
lt_id = lt_response['LaunchTemplate']['LaunchTemplateId']
print(f"Created launch template for the Application tier with ID {lt_id}")

# Create the load balancer for the Application Tier
lb_response = elbv2.create_load_balancer(
Name='AppTierLB',
Subnets=[subnet_id3, subnet_id4],
SecurityGroups=[app_sg_id],
Scheme='internal',
Type='application'
)
lb_arn = lb_response['LoadBalancers'][0]['LoadBalancerArn']
print(f"Created load balancer for the Application tier with ARN {lb_arn}")

# Create the target group for the application tier
tg_response = elbv2.create_target_group(
    Name='AppTierTG',
    Protocol='HTTP',
    Port=80,
    TargetType='instance',
    VpcId=vpc_id
)
tg_arn = tg_response['TargetGroups'][0]['TargetGroupArn']
print(f"Created target group for the Application tier with ARN {tg_arn}")

try:
    # Register the Application tier instances with the target group
    app_asg_response = autoscaling.create_auto_scaling_group(
        AutoScalingGroupName='AppTierASG',
        LaunchTemplate={
            'LaunchTemplateName': 'AppTierTemplate',
            'Version': '$Latest'
        },
        MinSize=3,
        MaxSize=10,
        TargetGroupARNs=[tg_arn],
        VPCZoneIdentifier=f"{subnet_id1},{subnet_id2}"
    )
    
    # Print the entire response for debugging purposes
    print(f"app_asg_response: {app_asg_response}")
    
    # Check if the 'AutoScalingGroup' key exists in the response dictionary
    if 'AutoScalingGroup' in app_asg_response:
        app_asg_name = app_asg_response['AutoScalingGroup']['AutoScalingGroupName']
        print(f"Created auto scaling group for the Application tier with name {app_asg_name}")
    else:
        print("Error: 'AutoScalingGroup' key not found in response.")
except Exception as e:
    print(f"Error creating auto scaling group: {e}")
# Create a DB subnet group
db_subnet_group_response = rds.create_db_subnet_group(
    DBSubnetGroupName='MyDBSubnetGroup',
    DBSubnetGroupDescription='Subnets for my RDS database',
    SubnetIds=[subnet_id5, subnet_id6]
)
db_subnet_group_name = db_subnet_group_response['DBSubnetGroup']['DBSubnetGroupName']
print(f"Created DB subnet group with name {db_subnet_group_name}")

# Create the RDS Database in the specified subnets
rds_response = rds.create_db_instance(
    DBName='MyDatabase',
    DBInstanceIdentifier='mydb',
    AllocatedStorage=20,
    Engine='mysql',
    EngineVersion='5.7',
    MasterUsername='admin',
    MasterUserPassword='password',
    DBInstanceClass='db.t2.micro',
    VpcSecurityGroupIds=[db_sg_id],
    MultiAZ=True,
    StorageType='gp2',
    BackupRetentionPeriod=7,
    PreferredBackupWindow='03:00-04:00',
    DBSubnetGroupName=db_subnet_group_name
)
rds_db_instance_id = rds_response['DBInstance']['DBInstanceIdentifier']
print(f"Created RDS database with ID {rds_db_instance_id}")

# Wait for the RDS instance to become available
waiter = rds.get_waiter('db_instance_available')
waiter.wait(DBInstanceIdentifier=rds_db_instance_id)

# Create a read replica of the RDS database in another availability zone
rds_response = rds.create_db_instance_read_replica(
    DBInstanceIdentifier='mydb-replica',
    SourceDBInstanceIdentifier=rds_db_instance_id,
    AvailabilityZone='us-east-2b'
)
rds_replica_instance_id = rds_response['DBInstance']['DBInstanceIdentifier']
print(f"Created RDS database read replica with ID {rds_replica_instance_id}")

print("3-Tiered Architecture was Successfully Launched")