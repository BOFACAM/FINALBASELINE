import pickle
import pandas as pd
from get_sbom import get_metrics
import os
import shutil
import openpyxl
from commons import data_storage_path, root_path


def check_log_files():
    """
    """
    output_path = os.path.join(root_path, "log_out.txt")
    error_path = os.path.join(root_path, "log_error.txt")

    if os.path.exists(output_path) or os.path.exists(error_path):
        with open(output_path, 'w+') as f:
            f.write('OUTPUT LOG FILE\n')
        f.close()
        with open(error_path, 'w+') as f:
            f.write('ERROR LOG FILE\n')
        f.close()


def main():
    
    # Check previous log files:
    check_log_files()    
    
    excel_file = "MS dataset.xlsx"
    df = pd.read_excel(excel_file)
    repo_names = df.iloc[:, 2].tolist()  # third column, from line 2 to line 10. Adjust the range as per your requirement

    # Run get_metrics to retrieve SBOM data
    all_metrics = get_metrics(repo_names)

    if all_metrics:
        # Save each repo's metrics as pickle file
        for metrics in all_metrics:
            repo_name = metrics["Full Name"]
            pickle_filename = f"{repo_name.replace('/', '_')}.pickle"
            if not os.path.exists(data_storage_path):
                os.mkdir(data_storage_path)
            with open(os.path.join(data_storage_path, pickle_filename), "wb") as f:
                pickle.dump(metrics, f)
            print(f"SBOM data for project repository '{repo_name}' saved as '{pickle_filename}'.")
    else:
        print("No metrics retrieved for any repository.")
    
    # With all the pickles generated, we zip the folder.
    shutil.make_archive(data_storage_path, 'zip', data_storage_path)
    if os.path.exists(os.path.join(root_path, "project-sboms.zip")):
        print("> ZIP file created") 
    else: 
        print("> ZIP file not created")

if __name__ == "__main__":
    main()
