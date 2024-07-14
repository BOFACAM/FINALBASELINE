import os
import re


working_id = ''
working_link = ''
#output_results = 'google_results.csv'
output_results = 'kubernetes-results.csv'
failed_path = 'failed_cloned_repos.txt'
debug_path = 'debug_.txt'
file_correlated = "correlated.txt"
file_flags_google= []
file_flags_kub = []

"""
Returns a list of all tokens or words split by whitespace.

@param content (str) : every character from a relevant file from the repository.

@returns tokens (list) :  a list of the 'tokens' or words seperated by white space from the file. 
"""
def tokenize_content(content):
    # Split the content by whitespace to get the tokens
    tokens = re.split(r'\s+', content)
    return tokens

"""
Given a list of tokens, and start and end tokens, returns a list of the subsection of tokens between the start and end.

@param tokens (list) : list of all tokens to be cropped
@param start_token (str) : the token that denotes the start of the subsection
@param end_token (str) : the token that denotes the end of the subsection

@returns 
    cropped_tokens (list) : a list of the subsection of tokens between the start and end tokens.
"""
def crop_tokens(tokens, start_token, end_token):
    # Find indices of the start and end tokens
    start_index = tokens.index(start_token) if start_token in tokens else None
    end_index = tokens.index(end_token) if end_token in tokens else None
    
    if start_index is not None and end_index is not None and start_index < end_index:
        # Crop the list from start_token to include end_token
        cropped_tokens = tokens[start_index:end_index + 1]
        print(cropped_tokens)
        return cropped_tokens
    else:
        return []

"""
Checks for syntax patterns and keywords for kubernetes and google and returns their flags for validation.

@param directory (file) : full path to a subdirectory within the home directory storing the cloned repository

@returns 
    kub_flag (int) : the flag denoting if the repository follows kubernetes standard template
    google_flag (int) : the flag denoting if the repository follows google standard template and syntax
"""
def check_keys_in_files(directory):
    global file_flags_google
    global file_flags_kub
    global google_flag
    global kub_flag
    correlating_file = ''
    # Traverse the directory and check each file
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.yaml') or file.endswith('.yml'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', errors='ignore') as f:
                    content = f.read()
                    # Tokenize the content
                    tokens = tokenize_content(content)
                    print( f"Tokens: {tokens}")
                    kub_flag = check_for_kubernetes_syntax(tokens)

                    # Crop tokens between 'resources:' and 'properties:'
                    rec_to_type = crop_tokens(tokens, 'resources:', 'type:')
                    print( f"Cropped Tokens: {rec_to_type}")
                    
                    if rec_to_type:
                        google_flag = check_for_gcdm_syntax(rec_to_type)

                        #FOR CHECKING KUBERNETES 
                        if kub_flag ==1:
                            google_flag = 0
                        
                        file_flags_google.append(google_flag)
                        file_flags_kub.append(kub_flag)
                        if google_flag == 1:
                            correlating_file = file
                            print( f"{working_link} {working_id} {correlating_file}")
                    else:
                        file_flags_google.append(0)
    
    if 1 in file_flags_google:
        google_flag = 1
    else:
        google_flag = 0
    
    if 1 in file_flags_kub:
        #if kub=1 and goog = 1 then goog = 0
        kub_flag = 1
        google_flag = 0
    else:
        kub_flag = 0

    return kub_flag, google_flag

"""
Checks the ordering of resources, name and type to ensure they occur in the same order, according to google syntax

@param tokens (list) : list of cropped tokens from resources to type

@returns (int) : flag denoting if the keys follow gcdm syntax.

"""
def check_for_gcdm_syntax(tokens):
    # Broad index-based check for GCDM keys in the correct order
    if 'resources:' in tokens:
        resources_index = tokens.index('resources:')
        if 'name:' in tokens[resources_index:] and 'type:' in tokens[resources_index:]:
            name_index = tokens[resources_index:].index('name:')
            type_index = tokens[resources_index:].index('type:')
            if name_index < type_index:  # Ensure the order is correct
                return 1
    return 0
"""
Checks if there are kubernetes specific keywords in the cropped list of tokens

@param tokens (list) : cropped list of tokens from resources to type.

@returns (int) : flag indicating if the kubernetes specific keys were found
"""
def check_for_kubernetes_syntax(tokens):
    # Define a set of Kubernetes-specific keys
    kubernetes_keys = {'apiVersion:', 'kind:', 'metadata:', 'spec:', 'containers:', 'replicas:', 'replicaCount:', 'selector:', 'template:'}
    
    # Check if any of these keys are present in the tokens
    if any(key in tokens for key in kubernetes_keys):
        return 1
    return 0

"""
Sets the kubernetes and google validation flags denoting if they follow syntax rules or contain specific keywords.

@param repo_dir (file) : full path to a subdirectory within the home directory storing the cloned repository

@return kub,goog (int,int) : flags denoting validation for kubernetes and google
"""
def kub_google_main(repo_dir):
    global file_flags_kub, file_flags_google
    kub, goog = check_keys_in_files(repo_dir)
    print({f"kubernetes"}, file_flags_kub, {f"goog"} ,file_flags_google)
    file_flags_google = []
    file_flags_kub = []
    return kub,goog
