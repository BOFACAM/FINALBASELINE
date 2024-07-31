import json
import os
import pandas as pd
prompt = ''
#Repo_id,URL,VAG,AWS,AZ,PUP,TF/OT,SS,PUL,BIC,DOCK,CHEF,GOOG,KUB,ANS,Validated files,IaC_tools
working_row = {
    "repo_id": '',
    "url":'',
    "Vagrant":0,
    "Amazon Web Services CloudFormation":0,
    "Azure DevOps":0,
    "Puppet ":0,
    "Terraform / Open Tofu":0,
    "Saltstack":0,
    "Pulumi":0,
    "Bicep":0,
    "Docker Compose":0,
    "Chef":0,
    "Google Cloud Deployment Manager":0,
    "Kubernetes":0,
    "Ansible":0,
    "files":None,
    "IAC_tools":[]
}
IAC_EXT = {
    "Terraform / Open Tofu" : ['.tf', '.tf.json'],#Terraform
    "Pulumi": ['.yaml', '.yml',],#Pulumi
    "Amazon Web Services CloudFormation": ['.yaml', '.yml', '.json'],#AWS CloudFormation
    "Azure DevOps": ['.json'],#Azure Resource Manager
    "Google Cloud Deployment Manager": ['.yaml'],#Google Cloud Deployment Manager
    "Chef": ['.rb'],#Chef
    "Puppet": ['.conf', '.pp'], #Puppet
    "Saltstack": ['.sls'],#SaltStack
    "Bicep": ['.bicep'],#Bicep
    "Vagrant": ['.vm', '.ssh', '.winrm', '.winssh', '.vagrant'],#VAG
    "Docker Compose":['.yaml','.yml'],#docker-compose.yaml
    "Kubernetes":['.yaml'],
    "Ansible": ['.yaml', '.yml','.cfg']#Ansible
}


jsonl = {}
# Path to your JSONL file
jsonl_file_path = 'data.jsonl'

def write_to_file(file_path, txt):
    with open(file_path, 'w') as file:
        file.write(txt)

# Function to append a dictionary to a JSONL file
def append_to_jsonl_file(dictionary, file_path):
    with open(file_path, 'a') as file:
        json.dump(dictionary, file)
        file.write('\n')

def extract_prefix(repo_id):
    return repo_id.split('_')[0]

def find_dependency_path(repo_id):
    prefix = extract_prefix(repo_id)
    base_dir = 'sbom-generator/project-dependencies'
    matching_path = None
    for root, dirs, files in os.walk(base_dir):
        for file_name in files:
            if prefix in file_name:
                matching_path = os.path.join(root, file_name)
                if matching_path:
                    #print(matching_path)
                    return matching_path
    return repo_id

def get_txt_list(repo_id):
    path = find_dependency_path(repo_id)
    if path and os.path.exists(path):
        with open(path, 'r') as file:
            lines = [line.strip() for line in file]
        return ', '.join(lines)
    else:
        write_to_file('error.txt',path + "\n")
        return "file not found"

def list_out_extensions(list_ext):
    if not list_ext:
        return ""
    if len(list_ext) == 1:
        return list_ext[0]
    
    str_ret = list_ext[0]
    for item in list_ext[1:]:
        str_ret = str_ret + " and " + item
    return str_ret

def json_main():
    # Path to your CSV file
    file_path = 'FINAL_TABLE.csv'

    # Read the CSV file into a DataFrame
    df = pd.read_csv(file_path)

    # Iterate through each row in the DataFrame
    for index, row in df.iterrows():
        #copy over each value to the working dict
        working_row["repo_id"]=row['Repo_id']
        working_row["url"]=row['URL']
        working_row["Vagrant"]=row['VAG']
        working_row["Amazon Web Services CloudFormation"]=row['AWS']
        working_row["Azure DevOps"]=row['AZ']
        working_row["Puppet"]=row['PUP']
        working_row["Terraform / Open Tofu"]=row['TF/OT']
        working_row["Saltstack"]=row['SS']
        working_row["Pulumi"]=row['PUL']
        working_row["Bicep"]=row['BIC']
        working_row["Docker Compose"]=row['DOCK']
        working_row["Chef"]=row['CHEF']
        working_row["Google Cloud Deployment Manager"]=row['GOOG']
        working_row["Kubernetes"]=row['KUB']
        working_row["Ansible"]= row['ANS']
        working_row["files"]=row['Validated files']
        working_row["Iac_tools"]=row["IaC_tools"]



        for key, value in working_row.items():
            if value == 1:
                #print("key:"+key)
                #print(working_row["repo_id"])
                txt_set = get_txt_list(working_row["repo_id"])
                ext_list = list_out_extensions(IAC_EXT[key])
                #print(ext_list)
                system = "Suppose you are an artifact installed on a server that provides Infrastructure as Code (IaC) configuration files. You have been given a list of dependencies with their versions from a GitHub repository named \"" + working_row["repo_id"] + "\" The project uses the " + key + " IaC tool. Your task is to analyze the provided list of dependencies and generate the corresponding " + key + " configuration files in the following formats: "+ ext_list+ "."
                user = "Generate the following " + key + " configuration files based on the provided list of dependencies: " + txt_set + " .Please ensure that each file is correctly formatted according to " + key + " standards and includes all necessary configurations based on the dependencies. For now just print the content of each file here in your response.Don't give any blurb,concisely just the file content. Give the entire file. Answer in the format x.extension: [file content] \n y.extension[file content], etc. where x,y match the IaC required file names.Give every file necessary for the IaC configuration. The extensions should be the ones as previously mentioned: " + ext_list + ". Please give every single file needed for configuration."
                new_json = {
                    "repo":working_row["repo_id"],
                    "iac_tool":key,
                    "system": {"role": "system", "content": system},
                    "user": {"role": "user", "content": user}
                    
                    #"system": system,
                    #"user":user,
                    #"role":"system"


                }
                
                #print(new_json)
                # Append the new dictionary to the JSONL file
                append_to_jsonl_file(new_json, jsonl_file_path)

#json_main()