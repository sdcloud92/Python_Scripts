
users = []

assert users == [], f"Expected 'users' to be [] but got: {repr(users)}"


users.append('kevin')
users.append('bob')
users.append('alice')

assert users == ['kevin', 'bob', 'alice'], f"Expected 'users' to be ['kevin', 'bob', 'alice'] but got: {repr(users)}"
del users[1]


assert users == ['kevin', 'alice'], f"Expected 'users' to be ['kevin', 'alice'] but got: {repr(users)}"

