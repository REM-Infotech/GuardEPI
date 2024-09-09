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
        # Tentativa de desinstalação do serviço, captura a saída e exibe
        result_uninstall = subprocess.run([f'{binary_name}', 'service', 'uninstall'], capture_output=True, text=True)
        print(f"Saída do comando de desinstalação:\n{result_uninstall.stdout}")
        if result_uninstall.stderr:
            print(f"Erros:\n{result_uninstall.stderr}")
    except Exception as e:
        print(f"Falha ao desinstalar o serviço: {e}")
        
    # Instalação do serviço, captura a saída e exibe
    result_install = subprocess.run([f'{binary_name}', 'service', 'install', token], capture_output=True, text=True)
    print(f"Saída do comando de instalação:\n{result_install.stdout}")
    if result_install.stderr:
        print(f"Erros:\n{result_install.stderr}")

if __name__ == "__main__":

    load_dotenv()
    token: str = os.getenv("CLOUDFLARED_TOKEN")
    if token and platform.system() == "Linux":
        
        configure_tunnel(token, install_cloudflared())

    from app import app
    debug = os.getenv('DEBUG', 'False').lower() in (
        'true', '1', 't', 'y', 'yes')

    app.run("0.0.0.0", 5002, debug, True)
