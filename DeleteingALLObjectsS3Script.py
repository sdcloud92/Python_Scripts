# Import the boto3 library to interact with Amazon Web Services (AWS)
import boto3

# Create an S3 client object to interact with the S3 service
s3 = boto3.client("s3")

# Get a list of objects in the specified S3 bucket
result = s3.list_objects(Bucket="Insert_Bucket_Name")

if result.get("Contents"):
    # Create a list of dictionaries, each containing the key of an object
    objects = [{"Key": obj["Key"]} for obj in result["Contents"]]

    # Delete all objects in the specified S3 bucket
    s3.delete_objects(Bucket="Insert_Bucket_Name", Delete={ "Objects": objects })

else:
    print("The specified bucket is empty.")
