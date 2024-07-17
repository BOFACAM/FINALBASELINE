import json
import os
import pandas as pd
prompt = ''
working_row = {
    "repo_id": '',
    "url":'',
    "VAG":0,
    "AWS":0,
    "AZ":0,
    "PUP":0,
    "TF/OT":0,
    "SS":0,
    "PUL":0,
    "BIC":0,
    "DOCK":0,
    "CHEF":0,
    "GOOG":0,
    "KUB":0,
    "files":None
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

def main():
    # Path to your CSV file
    file_path = 'FINAL_CSV.csv'

    # Read the CSV file into a DataFrame
    df = pd.read_csv(file_path)

    # Iterate through each row in the DataFrame
    for index, row in df.iterrows():
        #copy over each value to the working dict
        working_row["repo_id"]=row['Repo_id']
        working_row["url"]=row['URL']
        working_row["VAG"]=row['VAG']
        working_row["AWS"]=row['AWS']
        working_row["AZ"]=row['AZ']
        working_row["PUP"]=row['PUP']
        working_row["TF/OT"]=row['TF/OT']
        working_row["SS"]=row['SS']
        working_row["PUL"]=row['PUL']
        working_row["BIC"]=row['BIC']
        working_row["DOCK"]=row['DOCK']
        working_row["CHEF"]=row['CHEF']
        working_row["GOOG"]=row['GOOG']
        working_row["KUB"]=row['KUB']
        working_row["files"]=row['files']

        for key, value in working_row.items():
            if value == 1:
                print("key:"+key)
                sbom_path = find_sbom_path(working_row["repo_id"])
                new_json = {
                    "repo_id": working_row["repo_id"],
                    "url": working_row["url"],
                    "sbom_path":sbom_path,
                    "iac_tool":key
                }
                print(new_json)
                # Append the new dictionary to the JSONL file
                append_to_jsonl_file(new_json, jsonl_file_path)

        

    

main()