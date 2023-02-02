# Step 1 - Create an Empty List

aws_services_list = []

# Step 2 - Populate the List using append

aws_services_list.append('EC2')
aws_services_list.append('S3')
aws_services_list.append('Cloud9')
aws_services_list.append('Code_Commit')
aws_services_list.append('Lambda')
aws_services_list.append('API_Gateway')

# Step 3 - Print the list and the length of the list

print("AWS Service Inventory:", aws_services_list)
print("Number of Items in Inventory:", len(aws_services_list))

# Step 4 - Remove two specific services from the list by Name

aws_services_list.remove('EC2')
aws_services_list.remove('S3')

# Step 5 - Print the new list and new length of the list

print("AWS Service Inventory:", aws_services_list)
print("Number of Items in Inventory:", len(aws_services_list))