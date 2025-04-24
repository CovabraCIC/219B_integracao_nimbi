from models import DeltaServicos
from typing import Dict
from logs import logger

# Função para transformar serviço em formato JSON esperado pela API
def transform_delta_servicos_to_json(servico: DeltaServicos, codigoitem: str) -> Dict:
    logger.info(f"[{codigoitem}] Iniciando transformação do registro para JSON")
    try:
        result = {
            "Code": servico.codigoitem or "",
            "Description": servico.descricao_curta if servico.descricao_curta else "SEM DESCRITIVO",
            "LongDescription": servico.descricaolonga or "SEM DESCRITIVO",
            "LastPriceBuy": float(servico.precoultimacompra) if servico.precoultimacompra is not None else 0.0,
            "Type": servico.tipo or "",
            "UnitOfMeasureCode": servico.nome_da_unidade_medida if servico.nome_da_unidade_medida and servico.nome_da_unidade_medida != "--" else "UNIDADE",
            "Brand": servico.marca or "",
            "Model": servico.modelo or "",
            "SKU": servico.sku or "",
            "GTIN13": servico.gtin13 or "",
            "NCM": servico.ncm or "",
            "ManufacturerCode": servico.codigo_do_fabricante or ""
        }
        logger.info(f"[{codigoitem}] Transformação do registro para JSON concluida com sucesso")
        return result
    except Exception as e:
        logger.error(f"[{codigoitem}] Erro em transform_delta_serviços_to_json: {str(e)}")
        raise