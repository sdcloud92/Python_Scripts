# Import the boto3 library to interact with Amazon Web Services (AWS)
import boto3

# Create an S3 client object to interact with the S3 service
s3 = boto3.client("s3")

# Delete a single object in the specified S3 bucket
s3.delete_object(Bucket="Insert_Bucket_Name", Key='Insert_File_Name')

# Get a list of objects in the specified S3 bucket
objects = s3.list_objects(Bucket="Insert_Bucket_Name")["Contents"]

# Loop through the objects in the bucket
for obj in objects:
    # Delete each object in the bucket
    response = s3.delete_object(Bucket="Insert_Bucket_Name", Key=obj["Key"])
    # Print the response from the delete operation
    print(response)