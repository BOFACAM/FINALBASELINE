data_storage_path = "/home/mikel/projects/sbom-generator/project-sboms"
root_path = "/home/mikel/projects/sbom-generator/"


def write_statement(file, msg):
    with open(file, 'w+') as f:
            f.write('OUTPUT LOG FILE\n')