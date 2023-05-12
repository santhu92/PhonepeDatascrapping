import subprocess
command = "streamlit run streamlitdashboard.py"
subprocess.Popen(['cmd', '/c', command])
subprocess.wait()
