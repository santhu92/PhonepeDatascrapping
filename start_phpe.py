import subprocess
import os

scripts = ["phpeEDA.py", "Triggerstreamlit.py", ""]

# Iterate over the scripts and run them using subprocess
for script in scripts:
    subprocess.Popen(["python", script])

# Wait for all the subprocesses to complete
subprocess.wait()

