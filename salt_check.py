import os
import subprocess
import sys
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

output_results= 'salt_results.csv'
wworking_link = ''
working_id = ''
failed_path = 'failed_clones_ansible'

 # Look for common SaltStack files and directories
saltstack_files = ['top.sls', 'minion', 'minion.d']
saltstack_dirs = ['salt', 'pillar']
found_files = []
found_dirs = []


"""
Runs salt-lint parser on a given directory to decide if it is using SaltStack

@param directory (file) : full path to a subdirectory within the home directory storing the cloned repository

@return (int) flag determining if the repository is using Saltstack
"""
def run_salt_lint(directory):
    try:
        result = subprocess.run(['salt-lint', directory], capture_output=True, text=True)
        if result.returncode == 0:
            print("No SaltStack linting issues found.")
            return 1
        else:
            print("SaltStack linting issues found:")
            print(result.stdout)
            return 1
    except FileNotFoundError:
        print("salt-lint is not installed. Please install it using 'pip install salt-lint'.")
        sys.exit(1)

"""
Traverses the given repository for files ending in the Saltstack extensions and appends those to found_files.
Traverses the directories in the repository for directories that are specific to Saltstack,and appends their paths to found_dirs.

@param repo_dir (file) : full path to a subdirectory within the home directory storing the cloned repository
"""
def populate_found_elements(repo_dir):
    global found_dirs
    global found_files
    for root, dirs, files in os.walk(repo_dir):
        for file in files:
            if file in saltstack_files or file.endswith('.sls'):
                found_files.append(os.path.join(root, file))
        for dir in dirs:
            if dir in saltstack_dirs:
                found_dirs.append(os.path.join(root, dir))

"""
Gets the salt lint result. Populates validation lists with directory paths and saltstack files.

@param repo_dir (file) : full path to a subdirectory within the home directory storing the cloned repository

@returns flag (int) : flag denoting the successfulness of the salt-lint validation. 
"""
def salt_main(repo_dir):
    flag = run_salt_lint(repo_dir)
    populate_found_elements(repo_dir)

    if found_files or found_dirs:
        print("Found SaltStack files or directories:")
        flag = run_salt_lint(repo_dir)
    else:
        print("No SaltStack files or directories found.")
        flag = 0
    
    return flag
