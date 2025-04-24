from typing import Tuple, Dict
import requests
import json
import os
from logs import logger
from dotenv import load_dotenv

load_dotenv()

# Função para enviar serviço à API (POST)
def post_to_api(service: Dict, codigoitem: str) -> Tuple[bool, str]:
    try:
        API_URL = os.getenv("NIMBI_API_URL")
        headers = {
            "ClientAPI_ID": os.getenv("NIMBI_CLIENT_API_ID"),
            "ClientAPI_Key": os.getenv("NIMBI_CLIENT_API_KEY"),
            "OwnerUserName": os.getenv("NIMBI_OWNER_USERNAME"),
            "Content-Type": "application/json"
        }
        
        service_json = json.dumps(service, ensure_ascii=False)
        response = requests.post(API_URL, headers=headers, data=service_json)
        logger.info(f"[{codigoitem}] Requisição POST: {service_json}")
        return response.status_code in (200, 201), response.text
    except requests.RequestException as e:
        logger.error(f"[{codigoitem}] Erro na requisição POST: {str(e)}")
        return False, str(e)
    except Exception as e:
        logger.error(f"[{codigoitem}] Erro em send_to_api: {str(e)}")
        raise

# Função para atualizar serviço na API (PUT)
def put_to_api(service: Dict, codigoitem: str) -> Tuple[bool, str]:
    try:
        API_URL = os.getenv("NIMBI_API_URL")
        headers = {
            "ClientAPI_ID": os.getenv("NIMBI_CLIENT_API_ID"),
            "ClientAPI_Key": os.getenv("NIMBI_CLIENT_API_KEY"),
            "OwnerUserName": os.getenv("NIMBI_OWNER_USERNAME"),
            "Content-Type": "application/json",
            "ItemCode": codigoitem
        }
        
        service_json = json.dumps(service, ensure_ascii=False)
        response = requests.put(API_URL, headers=headers, data=service_json)
        logger.info(f"[{codigoitem}] Requisição PUT: {service_json}")
        return response.status_code in (200, 201), response.text
    except requests.RequestException as e:
        logger.error(f"[{codigoitem}] Erro na requisição PUT: {str(e)}")
        return False, str(e)
    except Exception as e:
        logger.error(f"[{codigoitem}] Erro em put_to_api: {str(e)}")
        raise