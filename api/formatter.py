from models import DeltaProdutos
from typing import Dict
from logs import logger

# Função para transformar produto em formato JSON esperado pela API
def transform_delta_produtos_to_json(produto: DeltaProdutos, codigoitem: str) -> Dict:
    logger.info(f"[{codigoitem}] Iniciando transformação do registro para JSON")
    try:
        result = {
            "Code": produto.codigoitem or "",
            "Description": produto.descricao_curta if produto.descricao_curta else "SEM DESCRITIVO",
            "LongDescription": produto.descricaolonga or "SEM DESCRITIVO",
            "LastPriceBuy": float(produto.precoultimacompra) if produto.precoultimacompra is not None else 0.0,
            "Type": produto.tipo or "",
            "UnitOfMeasureCode": produto.nome_da_unidade_medida if produto.nome_da_unidade_medida and produto.nome_da_unidade_medida != "--" else "UNIDADE",
            "Brand": produto.marca or "",
            "Model": produto.modelo or "",
            "SKU": produto.sku or "",
            "GTIN13": produto.gtin13 or "",
            "NCM": produto.ncm or "",
            "ManufacturerCode": produto.codigo_do_fabricante or ""
        }
        logger.info(f"[{codigoitem}] Transformação do registro para JSON concluida com sucesso")
        return result
    except Exception as e:
        logger.error(f"[{codigoitem}] Erro em transform_delta_produtos_to_json: {str(e)}")
        raise