# provides python support for Amazon Web Services (AWS) SDK

import boto3

# provides a way of using operating system dependent functionality.

import os

# provides a way of searching for files that match a specified pattern.

import glob

# sets the value of cwd to the current working directory and returns the cwd as a string

cwd = os.getcwd()

# appends the /upload/ directory to the current working directory, so cwd now represents the path to the upload directory.

cwd = cwd + "/upload/"

#  search for files that match the pattern cwd + "*.png". Result is a list of filenames, which is stored in the files variable.

files = glob.glob(cwd + "*.png")

# creates an s3 client object to interact with AWS services

s3 = boto3.client("s3")

# iterate over the files in the files list. On each iteration, the file variable will be set to the filename of the current file.

for file in files:
    s3.upload_file(
        Filename = file,
        Bucket = "Insert Bucket Name",
        Key = file.split("/")[-1])