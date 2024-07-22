import json
import os
import pandas as pd
prompt = ''
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
    "files":None
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
    "Kubernetes":['.yaml']
}



jsonl = {}
# Path to your JSONL file
jsonl_file_path = 'data.jsonl'

# Function to append a dictionary to a JSONL file
def append_to_jsonl_file(dictionary, file_path):
    with open(file_path, 'a') as file:
        json.dump(dictionary, file)
        file.write('\n')



def find_sbom_path(repo_id):
    base_dir='sbom-generator/project-sboms'
    file_name = repo_id + ".pickle"
    path = os.path.join(base_dir, file_name)
    
    if os.path.exists(path):
        return path
    else:
        return None

def jsonl_main():
    # Path to your CSV file
    file_path = 'FINAL_CSV.csv'

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
        working_row["files"]=row['files']



        for key, value in working_row.items():
            if value == 1:
                print("key:"+key)
                sbom_path = find_sbom_path(working_row["repo_id"])
                new_json = {
                    "repo_id": working_row["repo_id"],
                    "url": working_row["url"],
                    "sbom_path":sbom_path,
                    "iac_tool":key,
                    "extension": IAC_EXT["" +key]
                }
                print(new_json)
                # Append the new dictionary to the JSONL file
                append_to_jsonl_file(new_json, jsonl_file_path)
    return jsonl_file_path

        

    
#jsonl_main()