# File ~/.jupyter/jupyter_notebook_config.py
import subprocess, os, path

home_path = path.Path.home()
os.environ["PATH"] = f"{home_path}/.local/bin:" + os.environ["PATH"]
os.environ["KUBECONFIG"] = f"{home_path}/.kube/config.yaml"

try:
    # Run the command and capture the output
    result = subprocess.run(
        ["mise", "exec", "--", "bash", "-c", "echo $PATH"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=True
    )
    
    # The PATH value
    mise_path = result.stdout.strip()
    print("Mise PATH:", mise_path)
    os.environ["PATH"] = mise_path

except subprocess.CalledProcessError as e:
    print("Error executing command:")
    print(e.stderr)

