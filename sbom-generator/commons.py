"""
File with global variables for the sbom generation stage
"""

data_storage_path = "~/iac-parsers-24/sbom-generator/project-sboms"
root_path = "~/iac-parsers-24/sbom-generator/"


def write_statement(file, msg):
    with open(file, 'w+') as f:
            f.write('OUTPUT LOG FILE\n')