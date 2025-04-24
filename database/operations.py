from sqlalchemy.orm import Session
from datetime import datetime
from models.produtos import DeltaProdutos, SnapshotProdutos
from logs import logger
from sqlalchemy import select, update

def get_delta_products(session: Session, batch_size: int = 100):
    """
    Função para obter produtos de delta_produtos em lotes
    """
    logger.info("[N/A] Iniciando obtenção de registros da Delta.")
    try:
        offset = 0
        while True:
            logger.info(f"[N/A] Iniciando consulta com offset={offset}, batch_size={batch_size}")
            stmt = select(DeltaProdutos).offset(offset).limit(batch_size)
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

def insert_snapshot_product(session: Session, delta_produto: DeltaProdutos, codigoitem: str) -> None:
    """
    Função para inserir ou atualizar produto na Snapshot
    """
    try:
        logger.info(f"[{codigoitem}] Verificando existência na Snapshot")
        existing_record = session.execute(
            select(SnapshotProdutos).where(SnapshotProdutos.codigoitem == codigoitem)
        ).scalar_one_or_none()

        snapshot_data = {
            'codigoitem': codigoitem,
            'hash_dados': delta_produto.hash_atual,
            'descricao_curta': delta_produto.descricao_curta,
            'descricaolonga': delta_produto.descricaolonga,
            'precoultimacompra': delta_produto.precoultimacompra,
            'tipo': delta_produto.tipo,
            'marca': delta_produto.marca,
            'modelo': delta_produto.modelo,
            'sku': delta_produto.sku,
            'gtin13': delta_produto.gtin13,
            'ncm': delta_produto.ncm,
            'nome_da_unidade_medida': delta_produto.nome_da_unidade_medida,
            'codigo_do_fabricante': delta_produto.codigo_do_fabricante,
            'natureza_de_operacao': delta_produto.natureza_de_operacao,
            'status': delta_produto.status,
            'categoria_codigo_da_categoria': delta_produto.categoria_codigo_da_categoria,
            'nome_da_imagem': delta_produto.nome_da_imagem,
            'codigo_do_grupo_de_compras': delta_produto.codigo_do_grupo_de_compras,
            'data_atualizacao': datetime.now()
        }

        if existing_record:
            logger.info(f"[{codigoitem}] Registro encontrado na Snapshot, atualizando dados.")
            session.execute(
                update(SnapshotProdutos)
                .where(SnapshotProdutos.codigoitem == codigoitem)
                .values(**snapshot_data)
            )
        else:
            logger.info(f"[{codigoitem}] Nenhum registro encontrado na Snapshot, inserindo novo registro.")
            snapshot_record = SnapshotProdutos(**snapshot_data)
            session.add(snapshot_record)
        session.commit()
    except Exception as e:
        logger.error(f"[{codigoitem}] Exceção capturada no ato de inserção na Snapshot: {str(e)}")
        session.rollback()
        raise