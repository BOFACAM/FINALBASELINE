import os
import re
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
from tqdm import tqdm

working_id = ''
working_link = ''
output_results = 'pulumi_results.csv'
failed_path = 'failed_cloned_repos.txt'
debug_path = 'debugging.txt'

# Set your Pulumi access token here
PULUMI_ACCESS_TOKEN = 'pul-a31d7c8d3f43b8cce5a6e3f4ee015879f7ae3fce'


"""
Finds Pulumi specific file names in the given repository, and returns a list of the parent directories holding those files.

@param repo_path (file) : full path to a subdirectory within the home directory storing the cloned repository

@returns
    pulumi_files (list) : list of directories with a pulumi specific file name inside

"""

def find_pulumi_files(repo_path):
    pulumi_files = []
    for root, dirs, files in os.walk(repo_path):
        for dir in dirs:
            dir_path = os.path.join(root, dir)
            dir_files = os.listdir(dir_path)
            if 'Pulumi.yaml' in dir_files or 'Pulumi.lock.yaml' in dir_files:
                pulumi_files.append(dir_path)
    print(f"Found Pulumi files in directories: {pulumi_files}")
    return pulumi_files

"""
Runs pulumi parser on the repository

@param repo_path (file) : full path to a subdirectory within the home directory storing the cloned repository

@returns 
    (int) : flag determining if the pulumi parser was successful or not
"""
def check_pulumi_init(repo_path):
    try:
        env = os.environ.copy()
        env['PULUMI_ACCESS_TOKEN'] = PULUMI_ACCESS_TOKEN
        
        # Attempt to initialize the stack
        pulumi_cmd = shutil.which("pulumi")
        print(pulumi_cmd)
        result = subprocess.run(
            [pulumi_cmd, 'stack', 'init', '--stack', 'test-stack'],
            cwd=repo_path,
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        print(f"Pulumi init successful in {repo_path}")
        return 1
    
    except subprocess.CalledProcessError as e:
        error_message = e.stderr
        if "already exists" in error_message:
            print(f"Stack already exists, attempting to delete the existing stack: {error_message}")
            # Attempt to select and delete the existing stack
            try:
                select_result = subprocess.run(
                    ['pulumi', 'stack', 'select', '--stack', 'test-stack'],
                    cwd=repo_path,
                    env=env,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    check=True
                )
                delete_result = subprocess.run(
                    ['pulumi', 'stack', 'rm', '--stack', 'test-stack', '--yes'],
                    cwd=repo_path,
                    env=env,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    check=True
                )
                print(f"Pulumi stack deleted successfully. Re-initializing the stack.")
                # Re-attempt to initialize the stack
                init_result = subprocess.run(
                    ['pulumi', 'stack', 'init', '--stack', 'test-stack'],
                    cwd=repo_path,
                    env=env,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    check=True
                )
                print(f"Pulumi init successful in {repo_path}")
                return 1
            except subprocess.CalledProcessError as delete_error:
                print(f"Failed to delete existing Pulumi stack in {repo_path}\n{delete_error.stderr}")
                return 0
        else:
            print(f"Pulumi init failed in {repo_path}\n{error_message}")
            return 0


"""
First, gets the pulumi specific file directories. 
Then, runs Pulumi parser on the directory to obtain the truth flag for pulumi validation of the repository. 

@param repo_dir (file) : full path to a subdirectory within the home directory storing the cloned repository

@returns flag (int) : truth value representing if the pulumi parser was successful or unsuccessful in parsing.
"""
def pulumi_main(repo_dir):
    pulumi_dirs = find_pulumi_files(repo_dir)
    flag = 0 # changed this from original had to set flag before as flag is then used sometimes before it is initialzied 
    if pulumi_dirs:
        for dir in pulumi_dirs:
            if check_pulumi_init(dir) == 1:
                print("Pulumi stack initialized successfully.")
                flag = 1
    else:
        print("No Pulumi configuration files found.")
    return flag
        
