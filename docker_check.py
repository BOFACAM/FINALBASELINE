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

# result  = ''
# working_dockerfiles = []
failed_repo = 'failed_docker.txt'
output_results = 'docker_results.csv'
# success_flags = []

#result = []
#success_flags = []
#working_dockerfiles = []


"""
def find_docker_compose(root_dir):
    global working_dockerfiles
  
    for subdir, _, files in os.walk(root_dir):
        print(subdir, _, files)
        for file in files:
            if file in ['docker-compose.yml', 'docker-compose.yaml', 'compose.yaml']:
                full_path = os.path.join(subdir, file)
                print(full_path)
                working_dockerfiles.append(full_path)
    print(working_dockerfiles)
    if working_dockerfiles:
        final_eval = check_docker_compose_files()
        return final_eval
    else:
        return 0
"""

"""
def check_docker_compose_files():
    global working_dockerfiles
    global success_flags
    success_flags = []

    for file_path in working_dockerfiles:
        print(file_path)
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r',encoding="utf-8") as file:
                    yaml.safe_load(file)
                print(f"{file_path} is a valid Docker Compose file.")
                success_flags.append(1)
            except yaml.YAMLError as exc:
                print(f"{file_path} is not a valid Docker Compose file. Error: {exc}")
                success_flags.append(0)

        else:
            print(f"File not found: {file_path}")
            success_flags.append(0)

    print("Validation results:", success_flags)
    return 1 if 1 in success_flags else 0
"""

"""
Checking the validity of each file in the working_dockerfiles list.

@returns (int) : flag denoting if there were any valid docker files in the repository.

"""
def check_docker_compose_files(working_dockerfiles):

    success_flags = []

    for file_path in working_dockerfiles:
        print(file_path)
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r',encoding="utf-8") as file:
                    yaml.safe_load(file)
                print(f"{file_path} is a valid Docker Compose file.")
                success_flags.append(1)
            except yaml.YAMLError as exc:
                print(f"{file_path} is not a valid Docker Compose file. Error: {exc}")
                success_flags.append(0)

        else:
            print(f"File not found: {file_path}")
            success_flags.append(0)

    print("Validation results:", success_flags)
    return 1 if 1 in success_flags else 0

"""
Searches the given directory and its subdirectories for a file named 'docker-compose.yml'.
    
@param root_dir (str): The root directory of the repository to search.

@param bool: True if 'docker-compose.yml' is found, False otherwise.
"""
def find_docker_compose(root_dir, working_dockerfiles):

    for subdir, _, files in os.walk(root_dir):
        # print(subdir, _, files)
        for file in files:
            if file in ['docker-compose.yml', 'docker-compose.yaml', 'compose.yaml']:
                full_path = os.path.join(subdir, file)
                print(full_path)
                working_dockerfiles.append(full_path)
    # print(working_dockerfiles)
    if working_dockerfiles:
        final_eval = check_docker_compose_files(working_dockerfiles)
        return final_eval, working_dockerfiles
    else:
        return 0, []

"""
def docker_main(repo_dir):
    global result
    global success_flags
    global working_dockerfiles
    result = find_docker_compose(repo_dir)
    print(result)
    returning_dockerfile_paths = working_dockerfiles
    success_flags = []
    working_dockerfiles = []
    return result, returning_dockerfile_paths
"""

"""
Finds the result of the docker parsing mechanism 

@param repo_dir (file) : full path to a subdirectory within the home directory storing the cloned repository

@returns (int) : flag denoting if the repository likely uses docker
"""
def docker_main(repo_dir):

    working_dockerfiles = []
    result, docker_paths = find_docker_compose(repo_dir, working_dockerfiles)
    # print(result)
    # print(working_dockerfiles)
    #success_flags = []
    #b working_dockerfiles = []
    return result, docker_paths
