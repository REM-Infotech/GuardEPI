import os
import platform
import subprocess
import sys
from dotenv import load_dotenv


def install_cloudflared() -> str:

    os_name = platform.system().lower()
    print("Detectado Linux.")
    url = "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb"
    install_command = 'apt install ./cloudflared-linux-amd64.deb'
    binary_name = 'cloudflared'

    print(f"Baixando o Cloudflared para {os_name}...")
    subprocess.run(['curl', '-L', url, '-o', "cloudflared-linux-amd64.deb"])

    print(f"Instalando o Cloudflared para {os_name}...")
    subprocess.run(install_command, shell=True)

    print("Cloudflared instalado com sucesso.")
    return binary_name


def configure_tunnel(token: str, binary_name: str):
    
    print("Configurando o Cloudflared Tunnel...")
    
    try:
        subprocess.run([f'{binary_name}', 'service', 'uninstall'])
    except:
        pass
        
    subprocess.run([f'{binary_name}', 'service', 'install', token])


if __name__ == "__main__":

    load_dotenv()
    token: str = os.getenv("CLOUDFLARED_TOKEN")
    if token and platform.system() == "Linux":
        
        configure_tunnel(token, install_cloudflared())

    from app import app
    from configs import *

    app.run("0.0.0.0", 5002, debugmode(), True)
