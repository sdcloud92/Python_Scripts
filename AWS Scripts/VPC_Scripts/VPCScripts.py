import boto3

client = boto3.client("ec2")

#Creates VPC with particular CIDR Block
client.create_vpc(CidrBlock = '10.0.0.0/16')



