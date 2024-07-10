import pandas as pd
from git import Repo
import os
import subprocess
import shutil
import stat
from tqdm import tqdm
import json
import yaml
import csv

from salt_check import *
from pulumi_check import *
from bicep_check import *
from docker_check import *
   


#lets define the file extensions
IAC_TOOLS = {
    'TF': ['.tf', '.tf.json'],#Terraform
    'PUL': ['.yaml', '.yml',],#Pulumi
    'CP': ['.yaml', '.yml'],#Crossplane
    'AWS': ['.yaml', '.yml', '.json'],#AWS CloudFormation
    'AZ': ['.json'],#Azure Resource Manager
    'GOOG': ['.yaml'],#Google Cloud Deployment Manager
    'ANS': ['.yaml', '.yml','.cfg'],#Ansible
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

with open('iac_dataset.json') as f:
    json_data = json.load(f)

def read_csv(csv_file):
    df = pd.read_csv(csv_file)
    df = df[df["IS IAC FOUND?"] == True]
    return df

def get_home_directory(): #C:\Users\camyi 
    return os.path.expanduser("~")

def clone_repo(url, target_dir): #clones directory to target directory 
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
    else:
        return 
    repo = Repo.clone_from(url, target_dir)
    return repo


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

def is_meaningful_file(file_path):
    """
    Check if the file contains meaningful content (not empty, not just comments, or YAML separators).
    """
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

    clone_repo(repo_url, target_dir)
    
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

    return target_dir, relevant_files, row["IAC Tools"],repo_url

def validate_repo(row):
    target_dir, relevant_files, tools_found,repo_url = process_single_row(row)
    validated_files = []

    iac_dict = {
        "VAG": 0,
        "AWS": 0,
        "AZ": 0,
        "PUP": 0,
        "TF": 0,
        "SS": 0,
        "PUL": 0,
        "BIC":0,
        "DOCK":0
    }

    present,path = vagrant_validation(target_dir)
    if present:
        iac_dict["VAG"] = 1
        validated_files.append(path)
    
    tf_files = [f for f in relevant_files if f.endswith(('.tf', '.tf.json'))]
    aws_files = [f for f in relevant_files if f.endswith(('.yaml', '.yml', '.json'))]
    az_files = [f for f in relevant_files if f.endswith('.json')]
    pup_files = [f for f in relevant_files if f.endswith('.pp')]
  
    if 'AWS' in tools_found:
        appear, files = AWS_validation(aws_files)
        if appear:
            iac_dict["AWS"] = 1
            validated_files.extend(files)

    if 'AZ' in tools_found:
        appear, files = AZ_validation(az_files)
        if appear:
            iac_dict["AZ"] = 1
            validated_files.extend(files)

    if 'PUP' in tools_found:
        appear, files = PP_validation(pup_files)
        if appear:
            iac_dict["PUP"] = 1
            validated_files.extend(files)

    if 'TF' in tools_found:
        appear, files = init_validate_terraform_files(tf_files)
        if appear:
            iac_dict["TF"] = 1
            validated_files.extend(files)
    # end of my code

    if 'SS' in tools_found:
        salt_result = salt_main(target_dir)
        if salt_result:
            iac_dict["SS"] = 1
            validated_files.extend(found_files)
            validated_files.extend(found_dirs)

    if 'PUL' in tools_found:
        pulumi_result = pulumi_main(target_dir)
        if pulumi_result:
            iac_dict["PUL"] = 1
            validated_files.extend(find_pulumi_files(target_dir))
    
    if 'BIC' in tools_found:
        bicep_result,file_path = bicep_main(target_dir)
        if bicep_result:
            iac_dict['BIC'] = 1
            validated_files.append(file_path)
    
    if 'DOCC' in tools_found:
        docker_result = docker_main(target_dir)
        #docker_result will store a 0/1
        iac_dict["DOCK"]= docker_result
        #validated_files.extend(docker_files)
    if 'CH' in tools_found:
        chef_result = chef_main(target_dir)
        iac_dict["CHEF"] = chef_result
    
    shutil.rmtree(target_dir, onerror=onerror)
    return iac_dict, validated_files,repo_url

#VAGRANT
def vagrant_validation(target_dir):
    for root, dirs, files in os.walk(target_dir):
        if "Vagrantfile" in files:
            return True, os.path.join(root, "Vagrantfile")
    return False, None

#TERRAFORM
def init_validate_terraform_files(file_paths):
    validated_files=[]
    for file_path in file_paths:
        if is_meaningful_file(file_path):
            print(f"Validating Terraform file: {file_path}")
            try:
                temp_dir = os.path.join(os.path.dirname(file_path), 'temp_terraform_validate')
                os.makedirs(temp_dir, exist_ok=True)
                shutil.copy(file_path, temp_dir)
                init_result = subprocess.run(['terraform', 'init'], cwd=temp_dir, capture_output=True, text=True)
                if init_result.returncode != 0:
                    shutil.rmtree(temp_dir, onerror=onerror)
                    continue
                validate_result = subprocess.run(['terraform', 'validate'], cwd=temp_dir, capture_output=True, text=True)
                shutil.rmtree(temp_dir, onerror=onerror)
                if validate_result.returncode == 0:
                    validated_files.append(file_path)
                    return True,validated_files
            except FileNotFoundError or FileNotFoundError:
                print(f"file not found or not there")
            except Exception as e:
                print(e)
    return False,validated_files
        
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

#AZURE
def AZ_validation(file_paths):
    validated_files = []
    for file_path in file_paths:
        if is_meaningful_file(file_path):
            print(f"Validating Azure Resource Manager file: {file_path}")
            try:
                result = subprocess.run(['TemplateAnalyzer.exe', 'analyze-template', file_path], capture_output=True, text=True)
                if result.returncode == 0 or result.returncode not in {10, 20, 21, 22}:
                    validated_files.append(file_path)
                    return True,validated_files
            except FileNotFoundError or FileNotFoundError:
                print(f"file not found or not there")
            except Exception as e:
                print(e)
    return False,validated_files

#PUPPET
def PP_validation(file_paths):
    validated_files = []
    for file_path in file_paths:
        if is_meaningful_file(file_path):
            print(f"Validating Puppet manifest file: {file_path}")
            try:
                puppet_cmd = "puppet"
                puppet_path = shutil.which(puppet_cmd)
                
                result = subprocess.run([puppet_path,'parser', 'validate', file_path], capture_output=True, text = True)
                if result.returncode == 0:
                    validated_files.append(file_path)
                    return True,validated_files
            except FileNotFoundError or FileNotFoundError:
                print(f"file not found or not there")
            except Exception as e:
                print(e)
    return False,validated_files


def main():
    csv_file = "first_screening.csv"
    output_csv = "test_output.csv"

    df = read_csv(csv_file)


    with open(output_csv,'w') as file:
        writer = csv.writer(file)
        writer.writerow(["Repo_id", "URL", "VAG", "AWS", "AZ", "PUP", "TF/OT", "SS", "PUL","BIC","DOCK"])

    for i in tqdm(range(62,len(df))):
        row = df.iloc[i]
        repo_id = row["ID"]
        repo_url = row['URL']
        iac_dict,validated_files,repo_url= validate_repo(row)
        with open(output_csv,'a',newline ='') as f:
            validated_files_join = ';'.join(validated_files)
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
                        validated_files_join
                    ]
            writer.writerow(data_row)
    
main() 
