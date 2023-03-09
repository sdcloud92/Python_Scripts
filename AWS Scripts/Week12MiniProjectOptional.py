# imports needed dependencies for script

import random
import string

# function name, uses a loop to retrieve random alpha-string characters, attaches to assigned department, returns results to screen

def generate_names(number_of_names_needed, department):
    names = []
    for i in range(number_of_names_needed):
        name = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase, k=8))
        names.append(f"{name} ({department})")
    return names

# Assigns variables from user inputs, non-case-sensitive, returns prompt for invalid inputs, prints results to screen

number_of_names_needed = int(input("How many instance names do you require? "))
department = input("Assign a department (Marketing, Accounting, or FinOps): ").lower()

if department not in ["marketing", "accounting", "finops"]:
    print("You can only specify the following departments: Marketing, Accounting, or FinOps. Please try again and only specify a valid department.")
else:
    names = generate_names(number_of_names_needed, department.capitalize())
    print(names)