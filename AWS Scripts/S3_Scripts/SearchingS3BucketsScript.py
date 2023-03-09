import boto3

# creates a resource service client for Amazon S3.

resource = boto3.resource("s3")

# retrieves a list of all the S3 buckets associated with the AWS account and stores it in the variable bucket_list.

bucket_list = list(resource.buckets.all())

# returns the number of buckets in bucket_list.

len(bucket_list)

# loop that iterates through each bucket in bucket_list and prints the name of each bucket.

for bucket in resource/buckets.all():
    print(bucket.name)

