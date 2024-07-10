import csv
import shutil
import git
from git import Repo
import os
import pandas as pd
import yaml
import json

import pydriller as pydrill
from pydriller import Repository

import subprocess
from pathlib import Path

result  = ''

failed_repo = 'failed.txt'
output_results = 'chef_results.csv'


def run_foodcritic(cookbook_path):
    global result
    result = 0
    if not os.path.isdir(cookbook_path):
        print(f"Directory {cookbook_path} does not exist.")
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
        else:
            os.remove("foodcritic_output.txt")
            result =1
        
    except Exception as e:
        print(f"An error occurred while running Foodcritic: {e}")
    


def scan_for_cookbooks(repo_dir):
    global result
    """
    Scans the given repository directory for a subdirectory named 'cookbooks'.
    
    Args:
    repo_dir (str): The path to the repository directory.
    
    Returns:
    bool: True if 'cookbooks' directory is found, False otherwise.
    """
    cookbooks_dir = os.path.join(repo_dir, 'cookbooks')
    if os.path.isdir(cookbooks_dir):
        print(f"'cookbooks' directory found in {repo_dir}.")
        result = 1
        return cookbooks_dir
    else:
        print(f"'cookbooks' directory NOT found in {repo_dir}.")
        return repo_dir

def get_final_flag(repo_dir):
    new_dir = scan_for_cookbooks(repo_dir)
    flag = run_foodcritic(new_dir)
    return flag


def chef_main(repo_dir):
    global result
    result = get_final_flag(repo_dir)
    return result