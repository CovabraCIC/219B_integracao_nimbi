import socket
import os


def get_ip(): # Cria uma conexão temporária para um endereço externo (e. g., servidor DNS do Google)
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip_address = s.getsockname()[0]  # Obtém o IP associado à interface de saída
    except Exception:
        print("Erro ao tentar obter o IP.")
        ip_address = None
    finally:
        s.close()
    return ip_address


def dispatcher_ip_env(data=None):
    if os.getenv("IN_DOCKER"):  # Defina essa variável no container
        return '/mnt/pywin1/VariaveisAmbiente/.env'
    processors = {
        "10.95.7.13": r'\\10.95.7.13\pywin1\VariaveisAmbiente\.env',
        "10.95.7.12": r'\\10.95.7.13\pywin1\VariaveisAmbiente\.env',
        "10.95.7.40": '/mnt/pywin1/VariaveisAmbiente/.env'
    }
    processor = processors.get(data, r'\\10.95.7.13\pywin1\VariaveisAmbiente\.env')
    return processor
