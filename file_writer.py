import os
import re

all_llms = ["llama3","gemma","mistral","stablelm2","falcon2","dbrx", "vicuna"]
parent_file = "configuration_files_responses"
file_names = {
    "Vagrant":"Vagrant",
    "Amazon Web Services CloudFormation":"Amazon_Web_Services_CloudFormation",
    "Azure DevOps":"Azure_DevOps",
    "Puppet":"Puppet",
    "Terraform / Open Tofu":"Terraform_Open_Tofu",
    "Saltstack":"Saltstack",
    "Pulumi":"Pulumi",
    "Bicep":"Bicep",
    "Docker Compose":"Docker_Compose",
    "Chef":"Chef",
    "Google Cloud Deployment Manager":"Google_Cloud_Deployment_Manager",
    "Kubernetes":"Kubernetes",
    "Ansible":"Ansible"
}
unique_extensions = ['.tf', '.tf.json', '.yaml', '.yml', '.json', '.rb', '.conf', '.pp', '.sls', '.bicep', '.vm', '.ssh', '.winrm', '.winssh', '.vagrant', '.cfg']

def parse_response_llama(response):
    """
    Parses the response string and returns a dictionary where the keys are file names and values are file contents.
    
    :param response: The response string.
    :return: A dictionary with file names as keys and file contents as values.
    """
    pattern = re.compile(r'(\S+:\n```(?:.|\n)*?```)')
    matches = pattern.findall(response)
    
    response_dict = {}
    for match in matches:
        file_name, file_content = re.split(r':\n```', match)
        file_content = file_content.rsplit('```', 1)[0]
        response_dict[file_name.strip()] = file_content.strip()
    
    return response_dict

def configure_llama(response, path):
    """
    Configures Llama by writing parsed content to files in a nested directory structure.
    
    :param response: The response string.
    :param path: The base path where directories and files should be created.
    """
    response_dict = parse_response_llama(response)
    
    for file_name, content in response_dict.items():
        file_path = os.path.join(path, file_name)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w') as file:
            file.write(content)

def configure_gemma():
    return
def configure_mistral():
    return
def configure_stablelm2():
    return
def configure_falcon2():
    return
def configure_dbrx():
    return
def configure_vicuna():
    return

def write_files(response,id,iac_tool,llm):
    file_content = read_file_to_string(response)
    print(file_content)
     # Define the base path and nested directory structure
    base_path = 'configure'
    os.makedirs(base_path, exist_ok=True)
    
    with_id = os.path.join(base_path, id)
    if not os.path.exists(with_id):
        os.makedirs(with_id, exist_ok=True)
    
    with_iac = os.path.join(with_id, iac_tool)
    os.makedirs(with_iac, exist_ok=True)
    
    with_llm = os.path.join(with_iac, llm)
    os.makedirs(with_llm, exist_ok=True)

    print(with_llm)

    if llm == 'llama3':
        configure_llama(file_content,with_llm)
    elif llm == 'gemma':
        configure_gemma()
    elif llm == 'mistral':
        configure_mistral()
    elif llm == 'stablelm2':
        configure_stablelm2()
    elif llm == 'falcon2':
        configure_falcon2()
    elif llm == 'dbrx':
        configure_dbrx()
    elif llm == 'vicuna':
        configure_vicuna()


def read_file_to_string(file_path):
    """
    Reads the contents of a text file and returns it as a string.

    :param file_path: The path to the text file.
    :return: The contents of the file as a string.
    """
    try:
        with open(file_path, 'r') as file:
            file_content = file.read()
        
        print(file_content)
        return file_content
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
        return None

