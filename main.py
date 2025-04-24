from sqlalchemy.orm import Session
import json
from database import cic_engine
from sqlalchemy.orm.exc import ObjectDeletedError
from api import post_to_api, put_to_api
from api.formatter import transform_delta_servicos_to_json
from database.operations import get_delta_services, insert_snapshot_service
from logs import logger


def main() -> None:
    logger.info
    try:
        has_errors = False
        with Session(cic_engine, expire_on_commit=False) as session:  # Desativa expiração após commit
            for batch in get_delta_services(session, batch_size=1000):
                logger.info(f"[N/A] Iniciando processamento de lote com limite de {len(batch)} servicos.")
                for servico in batch:
                    try:
                        codigoitem = servico.codigoitem  # Acesso ao atributo pode falhar
                    except ObjectDeletedError as e:
                        logger.warning(f"[N/A] Erro: Objeto DeltaServicos deletado ou não presente: {str(e)}")
                        has_errors = False
                        continue
                    except Exception as e:
                        logger.error(f"[N/A] Erro ao acessar codigoitem do servico: {str(e)}")
                        has_errors = True
                        continue
                    logger.info(f"[{codigoitem}] Iniciando processamento do servico.")
                    try:
                        service_json = transform_delta_servicos_to_json(servico, codigoitem)
                        logger.info(f"[{codigoitem}] Conversão para JSON concluida com sucesso")
                        try:
                            success, response_text = post_to_api(service_json, codigoitem)
                        except Exception as e:
                            logger.error(f"[{codigoitem}] Erro na requisição POST: {str(e)}")
                            has_errors = True
                            continue
                        if success:
                            logger.info(f"[{codigoitem}] POST: Sucesso, Resposta: {response_text}")
                            try:
                                insert_snapshot_service(session, servico, codigoitem)
                            except Exception as e:
                                logger.error(f"[{codigoitem}] Falha ao inserir/atualizar Snapshot após POST: {str(e)}")
                                has_errors = True
                                continue
                        else:
                            try:
                                # Verificar se algum dos erros originados de requisição POST são devido itens existentes
                                response_json = json.loads(response_text) if response_text else {}
                                errors = response_json.get("errors", [])
                                if any(error.get("type") == "ExistConfig" and error.get("message") == "Code exist" for error in errors):
                                    logger.warning(f"[{codigoitem}] POST: Falha devido existência de objeto, Resposta: {response_text}")
                                    try:
                                        success, response_text = put_to_api(service_json, codigoitem)
                                        if success:
                                            logger.info(f"[{codigoitem}] PUT: Sucesso, Resposta: {response_text}")
                                            try:
                                                insert_snapshot_service(session, servico, codigoitem)
                                            except Exception as e:
                                                logger.error(f"[{codigoitem}] Falha ao inserir/atualizar Snapshot após PUT: {str(e)}")
                                                has_errors = True
                                                continue
                                        else:
                                            logger.error(f"[{codigoitem}] PUT: Falha, Resposta: {response_text}")
                                            has_errors = True
                                            continue
                                    except Exception as e:
                                        logger.error(f"[{codigoitem}] Erro na requisição PUT: {str(e)}")
                                        has_errors = True
                                        continue
                                else:
                                    logger.error(f"[{codigoitem}] POST: Falha, Resposta: {response_text}")
                                    has_errors = True
                                    continue
                            except json.JSONDecodeError:
                                logger.error(f"[{codigoitem}] Resposta da API não é um JSON válido: {response_text}")
                                has_errors = True
                                continue
                    except ObjectDeletedError as e:
                        logger.error(f"[{codigoitem}] Erro: Objeto DeltaServicos deletado ou não presente durante processamento: {str(e)}")
                        has_errors = True
                        continue
                    except Exception as e:
                        logger.error(f"[{codigoitem}] Erro ao processar servico: {str(e)}")
                        has_errors = True
                        continue
            
            if has_errors:
                logger.error("[N/A] Execução finalizada com erros. Verifique os logs para detalhes")
                exit(1)
            else:
                logger.success("[N/A] Execução finalizada sem erros")
        logger.info("[N/A] Finalizando process_services com sucesso")
    except Exception as e:
        logger.error(f"[N/A] Erro em process_services: {str(e)}")
        raise

if __name__ == "__main__":
    main()