import random
import string

def generate_names(num_names, department):
    names = []
    for i in range(num_names):
        name = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase, k=8))
        names.append(f"{name} ({department})")
    return names

num_names = int(input("How many instance names do you require? "))
department = input("Assign a department (Marketing, Accounting, or FinOps): ").lower()

if department not in ["marketing", "accounting", "finops"]:
    print("You can only specify the following departments: Marketing, Accounting, or FinOps. Please try again and only specify a valid department.")
else:
    names = generate_names(num_names, department.capitalize())
    print(names)