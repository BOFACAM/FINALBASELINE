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
working_dockerfiles = []
failed_repo = 'failed_docker.txt'
output_results = 'docker_results.csv'
success_flags = []

"""

def write_csv_header():
        with open(output_results, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['id', 'link', 'Docker'])  # Write header

def write_csv_file(id, link, result):
    with open(output_results, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([id, link, result])
"""



def find_docker_compose(root_dir):
    global working_dockerfiles
    """
    Searches the given directory and its subdirectories for a file named 'docker-compose.yml'.
    
    Args:
    root_dir (str): The root directory of the repository to search.
    
    Returns:
    bool: True if 'docker-compose.yml' is found, False otherwise.
    """
    for subdir, _, files in os.walk(root_dir):
        print(subdir, _, files)
        for file in files:
            if 'docker-compose.yml' in file:
                full_path = os.path.join(subdir, file)
                print(file)
                working_dockerfiles.append(full_path)
    print(working_dockerfiles)
    if working_dockerfiles:
        final_eval = check_docker_compose_files()
        return final_eval
    else:
        return 0

def check_docker_compose_files():
    global working_dockerfiles
    global success_flags
    success_flags = []

    for file_path in working_dockerfiles:
        print(file_path)
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r') as file:
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

def docker_main(repo_dir):
    global result
    global success_flags
    global working_dockerfiles
    result = find_docker_compose(repo_dir)
    print(result)
    success_flags = []
    working_dockerfiles = []
    return result 