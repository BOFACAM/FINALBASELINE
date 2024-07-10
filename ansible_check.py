import shutil
import os
import subprocess

def delete_dir():
    if os.path.exists('venv/output_file'):
        shutil.rmtree('venv/output_file')
        print(f"Directory {'venv/output_file'} has been removed.")
    else:
        print(f"Directory {'venv/output_file'} does not exist.")

def run_ansible_parser(repo_dir):
    try:
        # Run the ansible-content-parser command
        result = subprocess.run(['ansible-content-parser', repo_dir, 'venv/output_file'], capture_output=True, text=True)
        if result.returncode == 0:
            print("Ansible Content Parser ran successfully")
            print(result.stdout)
            delete_dir()
            return 1
        else:
            print("Ansible Content Parser failed")
            print(result.stderr)
            delete_dir()
            return 0
    except Exception as e:
        print(f"Failed to run Ansible Content Parser: {e}")
        delete_dir()
        return 2



def ansible_main(repo_dir):
    flag = run_ansible_parser(repo_dir)
    return flag

