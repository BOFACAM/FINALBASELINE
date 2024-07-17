"""
MORE INFORMATION ON THE PROCESS IN PAPER: https://zenodo.org/records/11100100

NOTE: If this code is used we need to cite this work.
"""

import time
import requests
import os
import openpyxl
from commons import data_storage_path, root_path, write_statement


def countdown(total):
    """
    Sets a countdown of 1h
    """

    while total:
        mins, secs = divmod(total, 60)
        timer = 'REMAINING: {:02d}:{:02d}'.format(mins, secs)
        print(timer, end='\r')
        time.sleep(1)
        total -= 1


def get_sbom_dependencies(full_name):
    token = "your-github-token"  # NOTE ON THIS
    try:
        # Make a request to the GitHub API for dependency graph SBOM
        url = f"https://api.github.com/repos/{full_name}/dependency-graph/sbom"
        headers = {"Authorization": f"token {token}"}
        print(f"Requesting SBOM from URL: {url}")
        response = requests.get(url, headers=headers)

        if int(response.headers['x-ratelimit-remaining']) < 10:
            print('SLEEPING TIME: 1H')
            countdown(3600)

        print(f"Response status code: {response.status_code}")
        dependencies = []
        # Check if the request was successful
        if response.status_code == 200:
            data = response.json()
            print(f"Response data: {data}")
            sbom = data.get("sbom", {})
            packages = sbom.get("packages", [])
            if packages:
                for package in packages:
                    name = package["name"]
                    dependencies.append(sbom)
                return dependencies
            else:
                print("No dependency information found in the SBOM.")
                write_statement(file=os.path.join(root_path, "log_error.txt"), msg=f"Dependencies not found for repo {full_name}.")
                return []
        else:
            print(f"Failed to fetch SBOM for {full_name}. Status code: {response.status_code} for URL: {url}")
            write_statement(file=os.path.join(root_path, "log_error.txt"), msg=f"Failed to fetch SBOM for {full_name}. Status code: {response.status_code} for URL: {url}")
            if response.status_code == 400:
                print("I will try again in 5 seconds...")
                time.sleep(5)
                return get_sbom_dependencies(full_name)
            return []
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        return []


def get_project_dependencies(repo_name):
    """
    Gets all the dependencies from the provided GitHub repository

    params: Repository name (str)
    """
    try:
        dependencies = get_sbom_dependencies(repo_name)
        if dependencies:
            write_statement(file=os.path.join(root_path, "log_out.txt"), msg=f"Dependencies found for repo {repo_name}.")
            return {
                "Full Name": repo_name,
                "Dependencies": dependencies
            }
            
        else:
            print(f"No dependencies found for {repo_name}.")
            write_statement(file=os.path.join(root_path, "log_error.txt"), msg=f"Dependencies not found for repo {repo_name}.")
            return None
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        return None


def get_metrics(repo_names):
    """
    Gets all the metrics from the provided list of GitHub repositories
    """
    all_metrics = []
    for repo_name in repo_names:
        print(f"Getting metrics for repo: {repo_name}")
        dependencies = get_project_dependencies(repo_name)
        if dependencies:
            all_metrics.append(dependencies)
            write_statement(file=os.path.join(root_path, "log_out.txt"), msg=f"Metrics retrieved for repo {repo_name}.")
        else:
            print(f"Failed to retrieve metrics for {repo_name}. Skipping...")
            write_statement(file=os.path.join(root_path, "log_error.txt"), msg=f"Failed to retrieve metrics for {repo_name}. Skipping...")

    return all_metrics

"""
if __name__ == "__main__":
    # Example list of repository names
    repo_names = [
        "RuoyuSu012/Office-Sitting-Posture-Detecting",
        "nvinayvarma189/Sitting-Posture-Recognition",
        # Add more repository names as needed
    ]

    all_metrics = get_metrics(repo_names)

    if all_metrics:
        # Save each repo's metrics as JSON file
        for metrics in all_metrics:
            repo_name = metrics["Full Name"]
            json_filename = f"{repo_name.replace('/', '_')}_sbom.json"
            with open(json_filename, "w") as f:
                json.dump(metrics, f, indent=4)
            print(f"SBOM file for project repository '{repo_name}' saved as '{json_filename}'.")
    else:
        print("No metrics retrieved for any repository.")
        """

