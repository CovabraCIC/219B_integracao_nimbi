from sqlalchemy.orm import Session
from datetime import datetime
from models.servicos import DeltaServicos, SnapshotServicos
from logs import logger
from sqlalchemy import select, update

def get_delta_services(session: Session, batch_size: int = 100):
    """
    Função para obter serviços de delta_serviços em lotes
    """
    logger.info("[N/A] Iniciando obtenção de registros da Delta.")
    try:
        offset = 0
        while True:
            logger.info(f"[N/A] Iniciando consulta com offset={offset}, batch_size={batch_size}")
            stmt = select(DeltaServicos).offset(offset).limit(batch_size)
            result = session.execute(stmt).scalars().all()
            if not result:
                break
            yield result
            offset += batch_size
            logger.info(f"[N/A] Finalizando iteração do lote com offset={offset}")
        logger.info("[N/A] Registros da Delta processados com sucesso")
    except Exception as e:
        logger.error(f"[N/A] Erro em obtenção dos registros da Delta: {str(e)}")
        raise

def insert_snapshot_service(session: Session, delta_servico: DeltaServicos, codigoitem: str) -> None:
    """
    Função para inserir ou atualizar serviço na Snapshot
    """
    try:
        logger.info(f"[{codigoitem}] Verificando existência na Snapshot")
        existing_record = session.execute(
            select(SnapshotServicos).where(SnapshotServicos.codigoitem == codigoitem)
        ).scalar_one_or_none()

        snapshot_data = {
            'codigoitem': codigoitem,
            'hash_dados': delta_servico.hash_atual,
            'descricao_curta': delta_servico.descricao_curta,
            'descricaolonga': delta_servico.descricaolonga,
            'precoultimacompra': delta_servico.precoultimacompra,
            'tipo': delta_servico.tipo,
            'marca': delta_servico.marca,
            'modelo': delta_servico.modelo,
            'sku': delta_servico.sku,
            'gtin13': delta_servico.gtin13,
            'ncm': delta_servico.ncm,
            'nome_da_unidade_medida': delta_servico.nome_da_unidade_medida,
            'codigo_do_fabricante': delta_servico.codigo_do_fabricante,
            'natureza_de_operacao': delta_servico.natureza_de_operacao,
            'status': delta_servico.status,
            'categoria_codigo_da_categoria': delta_servico.categoria_codigo_da_categoria,
            'nome_da_imagem': delta_servico.nome_da_imagem,
            'codigo_do_grupo_de_compras': delta_servico.codigo_do_grupo_de_compras,
            'data_atualizacao': datetime.now()
        }

        if existing_record:
            logger.info(f"[{codigoitem}] Registro encontrado na Snapshot, atualizando dados.")
            session.execute(
                update(SnapshotServicos)
                .where(SnapshotServicos.codigoitem == codigoitem)
                .values(**snapshot_data)
            )
        else:
            logger.info(f"[{codigoitem}] Nenhum registro encontrado na Snapshot, inserindo novo registro.")
            snapshot_record = SnapshotServicos(**snapshot_data)
            session.add(snapshot_record)
        session.commit()
    except Exception as e:
        logger.error(f"[{codigoitem}] Exceção capturada no ato de inserção na Snapshot: {str(e)}")
        session.rollback()
        raise