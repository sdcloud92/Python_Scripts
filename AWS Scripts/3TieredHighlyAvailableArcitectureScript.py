import boto3

# Set up the Boto3 EC2 and RDS clients
ec2 = boto3.client('ec2')
rds = boto3.client('rds')

# Create the VPC with a CIDR block of 10.10.0.0/16
vpc_response = ec2.create_vpc(CidrBlock='10.10.0.0/16')
vpc_id = vpc_response['Vpc']['VpcId']
print(f"Created VPC with ID {vpc_id}")

# Create the two public subnets in two different availability zones
subnet_response1 = ec2.create_subnet(VpcId=vpc_id, CidrBlock='10.10.1.0/24', AvailabilityZone='us-west-2a')
subnet_response2 = ec2.create_subnet(VpcId=vpc_id, CidrBlock='10.10.2.0/24', AvailabilityZone='us-west-2b')
subnet_id1 = subnet_response1['Subnet']['SubnetId']
subnet_id2 = subnet_response2['Subnet']['SubnetId']
print(f"Created public subnets with IDs {subnet_id1} and {subnet_id2}")

# Create the two private subnets in two different availability zones
subnet_response3 = ec2.create_subnet(VpcId=vpc_id, CidrBlock='10.10.3.0/24', AvailabilityZone='us-west-2a')
subnet_response4 = ec2.create_subnet(VpcId=vpc_id, CidrBlock='10.10.4.0/24', AvailabilityZone='us-west-2b')
subnet_id3 = subnet_response3['Subnet']['SubnetId']
subnet_id4 = subnet_response4['Subnet']['SubnetId']
print(f"Created private subnets with IDs {subnet_id3} and {subnet_id4}")

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
{'IpProtocol': 'tcp', 'FromPort': 20, 'ToPort': 20, 'IpRanges': [{'CidrIp': '0.0.0.0/0'}]}
])

ec2.authorize_security_group_egress(GroupId=web_sg_id, IpPermissions=[{'IpProtocol': '-1', 'IpRanges': [{'CidrIp': '0.0.0.0/0'}]}])
print(f"Created security group for the Web tier with ID {web_sg_id}")

# Create the security group for the application tier
sg_response = ec2.create_security_group(GroupName='AppTierSG', Description='Security group for the Application tier', VpcId=vpc_id)
app_sg_id = sg_response['GroupId']
ec2.authorize_security_group_ingress(GroupId=app_sg_id, IpPermissions=[{'IpProtocol': 'tcp', 'FromPort': 80, 'ToPort': 80, 'UserIdGroupPairs': [{'GroupId': web_sg_id}]}])
ec2.authorize_security_group_egress(GroupId=app_sg_id, IpPermissions=[{'IpProtocol': '-1', 'IpRanges': [{'CidrIp': '0.0.0.0/0'}]}])
print(f"Created security group for the Application tier with ID {app_sg_id}")

# Create the security group for the RDS database tier
sg_response = ec2.create_security_group(GroupName='DBSG', Description='Security group for the Database tier', VpcId=vpc_id)
db_sg_id = sg_response['GroupId']
ec2.authorize_security_group_ingress(GroupId=db_sg_id, IpPermissions=[{'IpProtocol': 'tcp', 'FromPort': 3306, 'ToPort': 3306, 'UserIdGroupPairs': [{'GroupId': app_sg_id}]}])
ec2.authorize_security_group_egress(GroupId=db_sg_id, IpPermissions=[{'IpProtocol': '-1', 'IpRanges': [{'CidrIp': '0.0.0.0/0'}]}])
print(f"Created security group for the Database tier with ID {db_sg_id}")

#Create the load balancer for the Web Tier
lb_response = ec2.create_load_balancer(
Name='WebTierLB',
Subnets=[subnet_id1, subnet_id2],
SecurityGroups=[web_sg_id],
Scheme='internet-facing',
Type='application'
)
lb_arn = lb_response['LoadBalancers'][0]['LoadBalancerArn']
print(f"Created load balancer for the Web tier with ARN {lb_arn}")

#Create the target group for the Web Tier
tg_response = ec2.create_target_group(
Name='WebTierTG',
Protocol='HTTP',
Port=80,
TargetType='instance',
VpcId=vpc_id)
tg_arn = tg_response['TargetGroups'][0]['TargetGroupArn']
print(f"Created target group for the Web tier with ARN {tg_arn}")

# Register the Web tier instances with the target group
web_asg_response = ec2.create_auto_scaling_group(
AutoScalingGroupName='WebTierASG',
LaunchTemplate={
    'LaunchTemplateName': 'WebTierTemplate',
    'Version': '$Latest'},
MinSize=3,
MaxSize=10,
TargetGroupARNs=[tg_arn],
VPCZoneIdentifier=f"{subnet_id1},{subnet_id2}"
)
web_asg_name = web_asg_response['AutoScalingGroupName']
print(f"Created auto scaling group for the Web tier with name {web_asg_name}")

# Create the launch tempalte for the Web tier instances
lt_response = ec2.create_launch_template(
LaunchTemplateName='WebTierTemplate',
LaunchTemplateData={
'ImageId': 'ami-0c55b159cbfafe1f0', # Choose your own AMI ID
'InstanceType': 't2.micro',
'KeyName': 'my_keypair', # Choose your own key pair name
'SecurityGroupIds': [web_sg_id],
'UserData': '''#!/bin/bash
echo "Hello, World!" > /var/www/html/index.html
'''
}
)
lt_id = lt_response['LaunchTemplate']['LaunchTemplateId']
print(f"Created launch template for the Web tier with ID {lt_id}")

# Create the load balancer for the Application Tier
lb_response = ec2.create_load_balancer(
Name='AppTierLB',
Subnets=[subnet_id3, subnet_id4],
SecurityGroups=[app_sg_id],
Scheme='internal',
Type='application'
)
lb_arn = lb_response['LoadBalancers'][0]['LoadBalancerArn']
print(f"Created load balancer for the Application tier with ARN {lb_arn}")

# Create the target group for the application tier
tg_response = ec2.create_target_group(
Name='AppTierTG',
Protocol='HTTP',
Port=80,
TargetType='instance',
VpcId=vpc_id
)
tg_arn = tg_response['TargetGroups'][0]['TargetGroupArn']
print(f"Created target group for the Application tier with ARN {tg_arn}")

#Register the Application tier instances with the target group
app_asg_response = ec2.create_auto_scaling_group(
AutoScalingGroupName='AppTierASG',
LaunchTemplate={
'LaunchTemplateName': 'AppTierTemplate',
'Version': '$Latest'
},
MinSize=3,
MaxSize=10,
TargetGroupARNs=[tg_arn],
VPCZoneIdentifier=f"{subnet_id3},{subnet_id4}"
)
app_asg_name = app_asg_response['AutoScalingGroupName']
print(f"Created auto scaling group for the Application tier with name {app_asg_name}")

# Create the launch tempalte for the application tier instances
lt_response = ec2.create_launch_template(
LaunchTemplateName='AppTierTemplate',
LaunchTemplateData={
'ImageId': 'ami-0c55b159cbfafe1f0', # Choose your own AMI ID
'InstanceType': 't2.micro',
'KeyName': 'my_keypair', # Choose your own key pair name
'SecurityGroupIds': [app_sg_id],
'UserData': '''#!/bin/bash
echo "Hello, World!" > /var/www/html/index.html
'''
}
)
lt_id = lt_response['LaunchTemplate']['LaunchTemplateId']
print(f"Created launch template for the Application tier with ID {lt_id}")

# Create the RDS Database
rds_response = rds.create_db_instance(
DBName='MyDatabase',
DBInstanceIdentifier='mydb',
AllocatedStorage=20,
Engine='mysql',
EngineVersion='5.7',
MasterUsername='admin',
MasterUserPassword='password',
DBInstanceClass='db.t2.micro',
VpcSecurityGroups=[db_sg_id],
MultiAZ=True,
AvailabilityZone='us-west-2a',
StorageType='gp2',
BackupRetentionPeriod=7,
PreferredBackupWindow='03:00-04:00'
)
rds_db_instance_id = rds_response['DBInstance']['DBInstanceIdentifier']
print(f"Created RDS database with ID {rds_db_instance_id}")

# Create a read replica of the RDS database in another availability zone
rds_response = rds.create_db_instance_read_replica(
DBInstanceIdentifier='mydb-replica',
SourceDBInstanceIdentifier=rds_db_instance_id,
AvailabilityZone='us-west-2b'
)
rds_replica_instance_id = rds_response['DBInstance']['DBInstanceIdentifier']
print(f"Created RDS database read replica with ID {rds_replica_instance_id}")