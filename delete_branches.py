import subprocess

def delete_branches():
    # Get the list of all branches
    branches = subprocess.check_output(["git", "branch"]).decode("utf-8").split("\n")
    # Get the name of the current branch
    current_branch = subprocess.check_output(["git", "rev-parse", "--abbrev-ref", "HEAD"]).decode("utf-8").strip()

    # Loop through the branches
    for branch in branches:
        branch = branch.strip()
        # Skip the "main" branch, the current branch, and branches that don't start with "thoglund"
        if branch == "main" or branch == current_branch or not branch.startswith("thoglund"):
            continue
        
        # Delete the branch
        subprocess.call(["git", "branch", "-D", branch])
        
        # Print a confirmation message
        print(f"Deleted branch: {branch}")
        
delete_branches()
