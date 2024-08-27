from dotenv import dotenv_values
from uuid import uuid4
import subprocess
import platform
import os

from datetime import timedelta

login_db = dotenv_values()['login']
passwd_db = dotenv_values()['password']
host_db = dotenv_values()['host']
database_name = dotenv_values()['database']

## PARAMETROS PARA O APP FLASK
DOCS_PATH = os.path.join(os.getcwd(), "Docs")
TEMP_PATH = os.path.join(os.getcwd(), "Temp")
IMAGE_TEMP_PATH = os.path.join(TEMP_PATH, "IMG")
CSV_TEMP_PATH = os.path.join(TEMP_PATH, "csv")
PDF_TEMP_PATH = os.path.join(TEMP_PATH, "pdf")
SQLALCHEMY_DATABASE_URI = f"mysql://{login_db}:{passwd_db}@{host_db}/{database_name}"
SQLALCHEMY_TRACK_MODIFICATIONS = False   
PREFERRED_URL_SCHEME = "https"
SESSION_COOKIE_HTTPONLY = False
SESSION_COOKIE_SECURE = True
PERMANENT_SESSION_LIFETIME = timedelta(days=7).max.seconds
SRC_IMG_PATH = os.path.join(os.getcwd(), "app", "src", "assets", "img")
SECRET_KEY = str(uuid4())

for paths in [DOCS_PATH, TEMP_PATH, IMAGE_TEMP_PATH, CSV_TEMP_PATH, PDF_TEMP_PATH]:
    
    if not os.path.exists(paths):
        os.makedirs(paths, exist_ok=True)
        
    else:
        
        plataforma = platform.system()
        
        if plataforma == "Linux":
            path =  f"{paths}/*" 
            comand = "rm -r " + path
             
        
        elif plataforma == "Windows":
            path =  f"{paths}\\*" 
            command = "powershell rm -r " + path
        
        os.system(command)


