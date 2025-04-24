from typing import Tuple, Dict
import requests
import json
import os
from logs import logger
from dotenv import load_dotenv

load_dotenv()

# Função para enviar produto à API (POST)
def post_to_api(product: Dict, codigoitem: str) -> Tuple[bool, str]:
    try:
        API_URL = "https://api01-qa.nimbi.net.br/API/rest/CatalogItemV2/v2/buy"
        headers = {
            "ClientAPI_ID": os.getenv("NIMBI_CLIENT_API_ID"),
            "ClientAPI_Key": os.getenv("NIMBI_CLIENT_API_KEY"),
            "OwnerUserName": os.getenv("NIMBI_OWNER_USERNAME"),
            "Content-Type": "application/json"
        }
        
        product_json = json.dumps(product, ensure_ascii=False)
        response = requests.post(API_URL, headers=headers, data=product_json)
        logger.info(f"[{codigoitem}] Requisição POST: {product_json}")
        return response.status_code in (200, 201), response.text
    except requests.RequestException as e:
        logger.error(f"[{codigoitem}] Erro na requisição POST: {str(e)}")
        return False, str(e)
    except Exception as e:
        logger.error(f"[{codigoitem}] Erro em send_to_api: {str(e)}")
        raise

# Função para atualizar produto na API (PUT)
def put_to_api(product: Dict, codigoitem: str) -> Tuple[bool, str]:
    try:
        API_URL = "https://api01-qa.nimbi.net.br/API/rest/CatalogItemV2/v2/buy"
        headers = {
            "ClientAPI_ID": os.getenv("NIMBI_CLIENT_API_ID"),
            "ClientAPI_Key": os.getenv("NIMBI_CLIENT_API_KEY"),
            "OwnerUserName": os.getenv("NIMBI_OWNER_USERNAME"),
            "Content-Type": "application/json",
            "ItemCode": codigoitem
        }
        
        product_json = json.dumps(product, ensure_ascii=False)
        response = requests.put(API_URL, headers=headers, data=product_json)
        logger.info(f"[{codigoitem}] Requisição PUT: {product_json}")
        return response.status_code in (200, 201), response.text
    except requests.RequestException as e:
        logger.error(f"[{codigoitem}] Erro na requisição PUT: {str(e)}")
        return False, str(e)
    except Exception as e:
        logger.error(f"[{codigoitem}] Erro em put_to_api: {str(e)}")
        raise