import pandas as pd
from git import Repo, GitCommandError
import os
import subprocess
import shutil
import stat
from tqdm import tqdm
import json
import yaml
import csv
import multiprocessing

from salt_check import *
from pulumi_check import *
from bicep_check import *
from docker_check import *
from chef_check import *
from kub_google_check import *
from ansible_check import *


"""
Each IAC tool and their corresponding file types.
"""
IAC_TOOLS = {
    'TF': ['.tf', '.tf.json'],#Terraform
    'PUL': ['.yaml', '.yml',],#Pulumi
    'CP': ['.yaml', '.yml'],#Crossplane
    'AWS': ['.yaml', '.yml', '.json'],#AWS CloudFormation
    'AZ': ['.json'],#Azure Resource Manager
    'GOOG': ['.yaml'],#Google Cloud Deployment Manager
    'ANS': ['.yaml', '.yml','.cfg'], #Ansible
    'CH': ['.rb'],#Chef
    'PUP': ['.conf', '.pp'], #Puppet
    'SS': ['.sls'],#SaltStack
    'BIC': ['.bicep'],#Bicep
    'OT': ['.tf', '.tf.json'],#OpenTofu
    'VAG': ['.vm', '.ssh', '.winrm', '.winssh', '.vagrant'],#VAG
    'DOCC':['.yaml','.yml'],#docker-compose.yaml
    'PAC':['.hcl', '.json'],#pkr.hcl or pkr.json
    'SaltStack':['.sls']
}

"""
Each IAC tool and their corresponding unique key identifiers in their files.
"""
UNIQUE_KEYS = {
    'Terraform': ['resource', 'provider', 'variable', 'output', 'data','locals'],
    'Pulumi': ['name', 'runtime', 'description', 'config', 'main'],
    'Crossplane': ['apiVersion', 'kind', 'metadata', 'spec'],
    'AWS CloudFormation': ['AWSTemplateFormatVersion', 'Resources', 'Outputs'],
    'Azure Resource Manager': ['$schema', 'contentVersion', 'resources'],
    'Google Cloud Deployment Manager': ['resources', 'imports'],
    'Ansible': ['name', 'hosts', 'vars', 'tasks'],
    'Chef': ['file', 'name', 'action'],
    'Puppet': ['file', 'service', 'package', 'node', 'class'],
    'SaltStack': ['pkg.installed', 'service.running', 'file.managed'],
    'Bicep': ['targetScope', 'param', 'var', 'resource', 'module', 'output'],
    'OpenTofu': ['resource', 'module', 'provider'],
    'Vagrant': ['Vagrant.configure', 'config.vm.box', 'config.vm.network'],
    'Docker Compose': ['version','services','volumes'],
    'Packer': ['source','variable','locals','build','data','builders'],
    'Kubernetes': ['apiVersion', 'kind', 'metadata', 'spec',]
}

"""
Open JSON file containing all repositories and their relevant information.
"""
with open('iac_dataset.json') as f:
    json_data = json.load(f)

"""
Given the CSV file of the first screening, returns the repositories that have tested positive for an IAC tool.

@param csv_file (file) : CSV file with repositories and their correlating 'IS IAC FOUND?' fields

@returns : Dataframe containing the repositories that have tested positive for an IAC tool. 
"""
def read_csv(csv_file):
    df = pd.read_csv(csv_file)
    df = df[df["IS IAC FOUND?"] == True]
    return df

"""
Returns the home directory.

@returns : Home directory of the location of the current project.

"""
def get_home_directory(): #C:\Users\camyi 
    return os.path.expanduser("~")


"""
Clones a repository into a target directory.

@param url (str)  : the url of the repository to be cloned.

@param target_dir (file) : full path to a subdirectory within the home directory, directory to store the cloned repository.

@returns : an instance of the Git repository, including its branches, commits, tags, configuration, and working directory. 
"""
def clone_repo(url, target_dir): #clones directory to target directory 
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
    else:
        return 
    repo = Repo.clone_from(url, target_dir)
    return repo

"""
Handles errors in the removal of a directory using 'shutil.rmtree'. 
Will check if the error is an access error and if so, will modify permissions and run the function again, else, will re-raise an error.

@param func (function) : Function that raised an exception.

@param path (str) : path to the directory that shutil.rmtree is removing.

@param exc_info (tuple) : exception information returned by `sys.exc_info()`.
"""
def onerror(func, path, exc_info):
    """
    Error handler for ``shutil.rmtree``.

    If the error is due to an access error (read-only file)
    it attempts to add write permission and then retries.

    If the error is for another reason it re-raises the error.
    
    Usage: ``shutil.rmtree(path, onerror=onerror)``
    """
    # Is the error an access error?
    if not os.access(path, os.W_OK):
        os.chmod(path, stat.S_IWUSR)
        func(path)
    else:
        raise

"""
Check if the file contains meaningful content (not empty, not just comments, or YAML separators).

@param file_path (str) : path to the file to be checked

@returns : a boolean flag denoting if the file is meaningful
"""
def is_meaningful_file(file_path):

    if not os.path.exists(file_path):  # In case the initially collected files have been deleted or modified.
        return False

    if os.path.getsize(file_path) == 0:
        return False
    try:
        with open(file_path, 'r',encoding='utf-8') as file:
            lines = file.readlines()
            content = ''.join(lines).strip()
            content_no_whitespace = ''.join(content.split())
            if content_no_whitespace =="{}":
                return False
            for line in lines:
                stripped_line = line.strip()
                if stripped_line and not stripped_line.startswith('#') and stripped_line != "---":
                    return True
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
    return False

"""
Retrieves the id, url, and raw json data from a row in the original CSV file. 
After confirming the presence of the raw json data, stores files and extensions and clones the repository.
Appends the files with an IAC relevant extension to a list. 

@param row (pandas.Series) : a single row of the repository dataframe

@returns 
    target_dir (file) : full path to a subdirectory within the home directory, directory to store the cloned repository.
    relevant_files (list) : list of file paths in the cloned repository that have the IAC relevant file extensions
    tools_found (list) : the field of the row that stores the list of abbreviated IAC tools. 
    repo_url (str) : the url for the Github repository 

"""
def process_single_row(row):
    repo_id = row["ID"]
    repo_url = row["URL"]
    raw_json_data = row["RAW_JSON_DATA"]

    if pd.isna(raw_json_data) or raw_json_data.strip() == '':
        raw_json_data = json_data.get(repo_id)
        if not raw_json_data:
            return None, None, None
    else:
        raw_json_data = json.loads(raw_json_data)

    files = raw_json_data["files"]
    found_extensions = raw_json_data["found_extensions"]
    target_dir = os.path.join(get_home_directory(), raw_json_data["id"].replace("\\", "/"))

    try:
        clone_repo(repo_url, target_dir)
    except GitCommandError as e:
        with open("log_error.txt", "a") as log_error:
            log_error.write(f"Repo: {repo_id}, Error: {e}\n")


    relevant_files = []
    for ext in found_extensions:
        if ext in files:
            for file_url in files[ext]:
                file_path = os.path.normpath(os.path.join(target_dir, file_url.replace(repo_url, '').lstrip('/')))
                print(f"Checking file path: {file_path}")
                if os.path.exists(file_path):
                    relevant_files.append(file_path)
                else:
                    print(f"File does not exist: {file_path}")

    return target_dir, relevant_files, row["IAC Tools"], repo_url, repo_id

"""
After obtaining the extension-relevant files, proceeds to validate the repository with 12 IAC parsing mechanisms.
If the IAC parser uses a list of files as a parameter, the method will populate validated_files with the files that validated the parser.

@param row (pandas.Series) : row symbolizing one Github repository from the dataframe containing all the repositories.

@return 
    iac_dict (dictionary) : a dictionary holding all the true/false (1/0) flags for each parser for a single repository
    validated_files (list) : a list of files that were validated when using a IAC parser that uses the relevant files for validation
    repo_url (str) : the url for the Github repository

"""
def validate_repo(row):
    target_dir, relevant_files, tools_found,repo_url, repo_id = process_single_row(row)
    validated_files = {}

    iac_dict = {
        "VAG": 0,
        "AWS": 0,
        "AZ": 0,
        "PUP": 0,
        "TF": 0,
        "SS": 0,
        "PUL": 0,
        "BIC": 0,
        "DOCK": 0,
        "CHEF": 0,
        "GOOG": 0,
        "KUB": 0,
        "ANS": 0
    }
    print(tools_found)

    present,path = vagrant_validation(target_dir)
    if present:
        iac_dict["VAG"] = 1
        validated_files["VAG"] = [path]
    
    tf_files = [f for f in relevant_files if f.endswith(('.tf', '.tf.json'))]
    aws_files = [f for f in relevant_files if f.endswith(('.yaml', '.yml', '.json'))]
    az_files = [f for f in relevant_files if f.endswith('.json')]
    pup_files = [f for f in relevant_files if f.endswith('.pp')]
    
    if 'ANS' in tools_found:
        ansible, ansible_paths = ansible_main(target_dir, repo_id)
        if ansible == 1:
            iac_dict["ANS"] = ansible
            validated_files["ANS"] = ansible_paths

    if 'AZ' in tools_found:
        #appear, files = AZ_validation(az_files)
        appear, files = AZ_validation_mac(az_files)
        
        # If you are using Mac OS, use this line instead of 'appear, files = AZ_validation(az_files)' : 
        # appear, files = AZ_validation_mac(az_files)
        if appear:
            iac_dict["AZ"] = 1
            validated_files["AZ"] = files
    
    if 'AWS' in tools_found:
        appear, files = AWS_validation(aws_files)
        if appear:
            iac_dict["AWS"] = 1
            validated_files["AWS"] = files

    if 'PUP' in tools_found:
        appear, files = PP_validation(pup_files)
        if appear:
            iac_dict["PUP"] = 1
            validated_files = files

    if 'TF' in tools_found: #good
        appear, files = init_validate_terraform_files(tf_files)
        if appear:
            iac_dict["TF"] = 1
            validated_files["TF"] = files
    # end of my code

    if 'SS' in tools_found: #good
        salt_result = salt_main(target_dir)
        if salt_result:
            iac_dict["SS"] = 1
            validated_files["SS"] = found_files
            validated_files["SS_dirs"] = found_dirs

    if 'PUL' in tools_found: #good
        pulumi_result = pulumi_main(target_dir)
        if pulumi_result:
            iac_dict["PUL"] = 1
            validated_files["PUL"] = find_pulumi_files(target_dir)
    
    if 'BIC' in tools_found:#good
        bicep_result, file_path = bicep_main(target_dir)
        if bicep_result:
            iac_dict['BIC'] = 1
            validated_files["BIC"] = [file_path]
    
    if 'DOCC' in tools_found: #good
        docker_result, file_paths = docker_main(target_dir)
        #docker_result will store a 0/1
        validated_files["DOCK"] = file_paths
        iac_dict["DOCK"] = docker_result
        #validated_files.extend(docker_files)
    if 'CH' in tools_found:#good
        chef_result = chef_main(target_dir)
        iac_dict["CHEF"] = chef_result
        
    if 'GOOG' or 'KUB' in tools_found:
        kubernetes, google = kub_google_main(target_dir)
        iac_dict["GOOG"] = google
        iac_dict["KUB"] = kubernetes
    
    shutil.rmtree(target_dir, onerror=onerror)
    return iac_dict, validated_files, repo_url

"""
Checks the repository for any files names 'Vagrantfile' as validation for the Vagrant IAC tool

@param target_dir (file) : full path to a subdirectory within the home directory

@returns 
    True : if has a file named 'Vagrantfile'
    False : if does not have a file named 'Vagrantfile'
"""
#VAGRANT
def vagrant_validation(target_dir):
    for root, dirs, files in os.walk(target_dir):
        if "Vagrantfile" in files:
            return True, os.path.join(root, "Vagrantfile")
    return False, None


def copy_file(source, dest):
    """
    Copies file into temporary location
    """

    try:
        shutil.copy(source, dest)
        return True
    except Exception as e:
        print(f"Error copying file: {e}")
        return False


"""
Runs a terraform validator (see README) on a file from the given list of file paths.

@param file_paths (list) : list of extension relevant file paths from the given repository

@returns 
    validated_files : a list of files that tested positive whilst validating terraform
    True : if there was a file encountered that tested positive for the terraform validation
    False : if there was no file found that tested positive for the terraform validation
"""

#TERRAFORM
def init_validate_terraform_files(file_paths):
    validated_files=[]
    for file_path in file_paths:
        if is_meaningful_file(file_path):
            print(f"Validating Terraform file: {file_path}")
            try:
                temp_dir = os.path.join(os.path.dirname(file_path), 'temp_terraform_validate')
                os.makedirs(temp_dir, exist_ok=True)

                # Monitorize the time the program takes to copy the file, if hung for 1 minute, then it jumps into next file.
                p = multiprocessing.Process(target=copy_file, args=(file_path, temp_dir))
                # shutil.copy(file_path, temp_dir)
                p.start()
                p.join(timeout=60)

                if p.is_alive():  # If the time went by and the file didn't get copied yet, there must be some permision issues, we skip.
                    p.terminate()
                    p.join()
                    print(f"> Terraform file {file_path} took too much time to get copied.")
                    shutil.rmtree(temp_dir, onerror=onerror)
                    continue

                init_result = subprocess.run(['terraform', 'init'], cwd=temp_dir, capture_output=True, text=True)
                if init_result.returncode != 0:
                    shutil.rmtree(temp_dir, onerror=onerror)
                    continue
                validate_result = subprocess.run(['terraform', 'validate'], cwd=temp_dir, capture_output=True, text=True)
                shutil.rmtree(temp_dir, onerror=onerror)
                if validate_result.returncode == 0:
                    validated_files.append(file_path)
                    return True, validated_files
            except FileNotFoundError or FileNotFoundError:
                print(f"file not found or not there")
            except Exception as e:
                print(e)
    return False, validated_files

"""
Runs cfn-lint AWS parser (see README) on the list of files from a single repository

@param file_paths (list) : list of extension relevant file paths from the given repository

@returns 
    validated_files : a list of files that tested positive whilst validating AWS
    True : if there was a file encountered that tested positive for the AWS validation
    False : if there was no file found that tested positive for the AWS validation
"""       
#AWS
def AWS_validation(file_paths):
    validated_files = []
    for file_path in file_paths:
        if is_meaningful_file(file_path):
            print(f"Validating AWS CloudFormation file: {file_path}")
            try:
                result = subprocess.run(['cfn-lint', file_path], capture_output=True, text=True)
                if result.returncode == 0 or result.returncode not in {2, 6, 10, 14}:
                    validated_files.append(file_path)
                    return True,validated_files
            except FileNotFoundError or FileNotFoundError:
                print(f"file not found or not there")
            except Exception as e:
                print(e)
    return False,validated_files

"""
Runs Azure TemplateAnalyzer (see README) on the list of files from a single repository

@param file_paths (list) : list of extension relevant file paths from the given repository

@returns 
    validated_files : a list of files that tested positive whilst validating Azure
    True : if there was a file encountered that tested positive for the Azure validation
    False : if there was no file found that tested positive for the Azure validation
"""

#AZURE
def AZ_validation(file_paths):
    validated_files = []
    for file_path in file_paths:
        if is_meaningful_file(file_path):
            print(f"Validating Azure Resource Manager file: {file_path}")
            try:
                result = subprocess.run(['TemplateAnalyzer.exe', 'analyze-template', file_path], capture_output=True, text=True)
                print(result)
                if result.returncode == 0 or result.returncode not in {10, 20, 21, 22}:
                    validated_files.append(file_path)
                    return True, validated_files
            except FileNotFoundError or FileNotFoundError:
                print(f"file not found or not there")
            except Exception as e:
                print(e)
    return False,validated_files
"""
Runs Azure TemplateAnalyzer for Mac OS (see README) on the list of files from a single repository

@param file_paths (list) : list of extension relevant file paths from the given repository

@returns 
    validated_files : a list of files that tested positive whilst validating Azure
    True : if there was a file encountered that tested positive for the Azure validation
    False : if there was no file found that tested positive for the Azure validation
"""

def AZ_validation_mac(file_paths):
    validated_files = []
    analyzer_cli_path = find_analyzer_cli_path()
    print(analyzer_cli_path)

    for file_path in file_paths:
        if is_meaningful_file(file_path):
            print(f"Validating Azure Resource Manager file: {file_path}")
            try:
                result = subprocess.run(['dotnet', 'run', '--', 'analyze-template', file_path],cwd=analyzer_cli_path,capture_output=True,text=True)
                if result:
                    print(result.stdout)
                    print(result.stderr)
                    if result.returncode == 0 or result.returncode not in {10, 20, 21, 22}:
                        validated_files.append(file_path)
                        print("AZURE : ")
                        print(result.returncode)
                        return True, validated_files
                    else:

                        print(result)
                        print("Result not valid")
            except FileNotFoundError:
                print(f"File not found: {file_path}")
            except Exception as e:
                print(f"An error occurred while validating {file_path}: {e}")
    return False, validated_files
"""
Finds azure template analyzer path, used for finding the Azure Template Analyzer Client on Mac OS configuration

@returns 
    analyzer_cli_path (str) : if analyzer client is properly initialized and built
    None : if analyzer client was not properly initialized and built

"""
def find_analyzer_cli_path():
    # Assuming the Analyzer.Cli is in the 'template-analyzer/src/Analyzer.Cli' directory relative to the current directory
    current_dir = os.getcwd()
    analyzer_cli_path = os.path.join(current_dir, 'template-analyzer', 'src', 'Analyzer.Cli')
    if os.path.exists(analyzer_cli_path):
        return analyzer_cli_path
    return None

"""
Runs Puppet parser (see README) on the list of files from a single repository

@param file_paths (list) : list of extension relevant file paths from the given repository

@returns 
    validated_files : a list of files that tested positive whilst validating Puppet
    True : if there was a file encountered that tested positive for the Puppet validation
    False : if there was no file found that tested positive for the Puppet validation
"""       
#PUPPET
def PP_validation(file_paths):#good
    validated_files = []
    for file_path in file_paths:
        if is_meaningful_file(file_path):
            print(f"Validating Puppet manifest file: {file_path}")
            try:
                puppet_cmd = "puppet"
                puppet_path = shutil.which(puppet_cmd)
                print(puppet_path)
                
                result = subprocess.run([puppet_path, 'parser', 'validate', file_path], capture_output=True, text=True)
                print(result.stdout)
                print(result.stderr)
                if result.returncode == 0:
                    validated_files.append(file_path)
                    return True,validated_files
            except FileNotFoundError or FileNotFoundError:
                print(f"file not found or not there")
            except Exception as e:
                print(e)
    return False,validated_files


"""
It adds a final output file with all the identified IaC tools per project
"""
def structure_final_file(unformatted_file):
 
    # Get the df
    df = pd.read_csv(unformatted_file)

    # Generate column for IaC tools
    df["IaC_tools"] = ''

    # Fill the new column with the IaC tools
    for ind in range(0, len(df)):
        iac_tools = []
        for col_ind in range(2, 16):  # Index numbers of the parser names in the pandas columns
            if df.iloc[ind, col_ind] == 1:
                colname = df.columns[col_ind]
                iac_tools.append(colname)
        df.iloc[ind, len(df.columns)-1] = ", ".join(iac_tools)

    df.to_csv(unformatted_file, index=False)



"""
Handles opening and writing to the output CSV.
Each subsequent column after 'URL' is a 0/1 flag denoting each IAC's usage. 
A column at the end stores the files validated by the parsers.
"""
def main():
    analyzer_path = find_analyzer_cli_path()
    print(analyzer_path)
    print("\nSTOP\n")
    csv_file = "first_screening.csv"
    output_csv = "FINAL_CSV_1.csv"
    df = read_csv(csv_file)

    if os.path.exists(output_csv):
        output_df = pd.read_csv(output_csv)
        starting_pro_index = len(output_df)
    else:
        with open(output_csv,'w') as file:
            writer = csv.writer(file)
            writer.writerow(["Repo_id", "URL", "VAG", "AWS", "AZ", "PUP", "TF/OT", "SS", "PUL", "BIC", "DOCK", "CHEF", "GOOG", "KUB", "ANS", "Validated files"])

        starting_pro_index = 0

    for i in tqdm(range(starting_pro_index, len(df))):  # 22 (for i in tqdm(range(0,len(df))):)
        row = df.iloc[i]
        repo_id = row["ID"]
        # repo_url = row['URL']
        iac_dict,validated_files, repo_url = validate_repo(row)
        with open(output_csv, 'a', newline='') as f:
            # validated_files_join = ';'.join(validated_files)
            writer = csv.writer(f)
            data_row = [repo_id,
                        repo_url, 
                        iac_dict["VAG"],
                        iac_dict["AWS"],
                        iac_dict["AZ"],
                        iac_dict["PUP"],
                        iac_dict["TF"],
                        iac_dict["SS"],
                        iac_dict["PUL"],
                        iac_dict["BIC"],
                        iac_dict["DOCK"],
                        iac_dict["CHEF"],
                        iac_dict["GOOG"],
                        iac_dict["KUB"],
                        iac_dict["ANS"],
                        validated_files
                    ]
            writer.writerow(data_row)

    structure_final_file(output_csv)
    
main() 
