import subprocess

subprocess.Popen(["uvicorn", "app.main:app", "--reload"])
subprocess.Popen(["streamlit", "run", "frontend/streamlit_app.py"])