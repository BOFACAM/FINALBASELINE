import csv
import os
import json

output_results = 'bicep_results.csv'
debug = 'debug_output.txt'
root_directory = 'ALL_REPO_JSON'  # Update this path if needed
bicep_flags = {}
"""
Processes a given repository directory to check for the presence of Bicep files.

@param repo_dir (str): The path to the repository directory to be processed.

@returns 
    has_bicep_files (int): 1 if a Bicep file is found, otherwise 0
    file_path (str): The path to the first Bicep file found if any, otherwise an undefined value
"""
def process_repo_for_bicep_files(repo_dir):
    has_bicep_files = 0
    for subdir, _, files in os.walk(repo_dir):
        for file in files:
            if file.endswith(".bicep"):
                has_bicep_files = 1
                file_path = os.path.join(subdir, file)
                break
        if has_bicep_files:#may change this to return validated file
            return has_bicep_files,file_path
            #break
    return has_bicep_files,file_path
"""
Extracts the 'id' and 'repo_link' from the given data dictionary.

@param data (dict): The input dictionary containing the data.

@returns tuple or None: A tuple (id, repo_link) if both keys are present, otherwise None.
"""
def get_id_repo_pair(data):
    if 'id' in data and 'repo_link' in data:
        return data['id'], data['repo_link']
    return None

"""
Checks for the presence of the 'BIC' tool in the list of used IaC tools and sets a flag.

@param data (dict): The input dictionary containing the data.

@returns flag (int): 1 if 'BIC' is in the list of IaC tools, otherwise 0
"""
def set_flag(data):
    if 'list_of_used_iac_tools' in data:
        list_iac_tools = data['list_of_used_iac_tools']
        with open(debug, 'a') as debug_file:
            debug_file.write(f"iac list: {list_iac_tools}\n")
        for tool in list_iac_tools:
           if tool == 'BIC':
               return 1
        return 0

"""
Obtains the flag denoting Bicep IAC usage and the path to the first found Bicep file. 

@param repo_dir (str): The path to the repository directory to be processed.

@returns 
    flag (int) : 0/1 value denoting if the repository uses bicep
    file_path (str) : the path to the bicep file in the repository
"""
def bicep_main(repo_dir):
    flag,file_path = process_repo_for_bicep_files(repo_dir)
    return flag,file_path
    
