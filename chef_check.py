import csv
import shutil
import git
from git import Repo
import os

import subprocess

result  = ''

failed_repo = 'failed.txt'
output_results = 'chef_results.csv'


"""
Runs foodcritic chef parser on a given cookbook.

@param cookbook_path (str) : the path of the cookbook inside the repository

@returns (int) : success or failure flag for running foodcritic on a cookbook
"""
def run_foodcritic(cookbook_path):
    if not os.path.isdir(cookbook_path):
        print(f"Directory {cookbook_path} does not exist.")
        return 0
    
    try:
        # Run the foodcritic command and write output to a text file
        result = subprocess.run(['foodcritic', cookbook_path], capture_output=True, text=True)
        
        with open('foodcritic_output.txt', 'w') as f:
            f.write(result.stdout)
            f.write(result.stderr)

        # Read the output from the text file
        with open('foodcritic_output.txt', 'r') as f:
            output = f.read()

        # Print the output of the command
        print("Foodcritic Output:")
        print(output)

        # Check the output for "Checking 0 files"
        if "Checking 0 files" in output:
            print(f"No files to check in the cookbook: {cookbook_path}")
            os.remove('foodcritic_output.txt')
            return 0
        else:
            os.remove("foodcritic_output.txt")
            return 1
        
    except Exception as e:
        print(f"An error occurred while running Foodcritic: {e}")
        return 0

"""
Scans the given repository directory for a subdirectory named 'cookbooks'.

@param repo_dir (str): The path to the repository directory.

@returns
    str: The path to the 'cookbooks' directory if found, otherwise the repo_dir.
    bool: True if 'cookbooks' directory is found, False otherwise.
"""
def scan_for_cookbooks(repo_dir):

    cookbooks_dir = os.path.join(repo_dir, 'cookbooks')
    if os.path.isdir(cookbooks_dir):
        print(f"'cookbooks' directory found in {repo_dir}.")
        return cookbooks_dir, True
    else:
        print(f"'cookbooks' directory NOT found in {repo_dir}.")
        return repo_dir, False

"""
Obtains the cookbook and runs foodcritic on it to obtain chef validation.

@param repo_dir (str): The path to the repository directory.

@returns (int) : flag representing success or failure in running foodcritic.
"""
def chef_main(repo_dir):
    cookbook_path, found = scan_for_cookbooks(repo_dir)
    if not found:
        return 0

    return run_foodcritic(cookbook_path)
