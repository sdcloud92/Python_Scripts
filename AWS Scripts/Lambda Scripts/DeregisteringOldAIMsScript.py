import datetime
from dateutil.parser import parse

import boto3


def days_old(date):
    # Calculate the number of days between the given date and today
    parsed = parse(date).replace(tzinfo=None)
    diff = datetime.datetime.now() - parsed
    return diff.days


def lambda_handler(event, context):

    # List of regions to search for AMIs
    regions = ['us-east-2']

    ami_deleted = False

    for region in regions:
        # Connect to EC2 client in the current region
        ec2 = boto3.client('ec2', region_name=region)
        print("Region:", region)

        # List all AMIs that are owned by the current account
        amis = ec2.describe_images(Owners=['self'])['Images']

        # Loop through all the AMIs and delete them if they are older than 2 days
        for ami in amis:
            creation_date = ami['CreationDate']
            age_days = days_old(creation_date)
            image_id = ami['ImageId']
            print('ImageId: {}, CreationDate: {} ({} days old)'.format(
                image_id, creation_date, age_days))

            if age_days >= 2:
                print('Deleting ImageId:', image_id)

                # Deregister the AMI
                ec2.deregister_image(ImageId=image_id)
                ami_deleted = True

    # If no AMIs were deleted, print a message
    if not ami_deleted:
        print("No AMIs were deleted.")