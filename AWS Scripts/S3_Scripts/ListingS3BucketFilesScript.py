# Import the boto3 library to interact with Amazon Web Services (AWS)

import boto3

# Create an S3 client object to interact with the S3 service

s3 = boto3.client("s3")

# Get a list of objects in the specified S3 bucket

objects = s3.list_objects(Bucket = "Insert_Bucket_Name")["Contents"]

# Check if there are any objects in the bucket

if len(objects) > 0:
    
    # Print a message if objects exist in the bucket
    
    print("objects_exist")

# Loop through the objects in the bucket

for obj in objects:
   
    # Print the key (filename) of each object
   
    print(obj["Key"])