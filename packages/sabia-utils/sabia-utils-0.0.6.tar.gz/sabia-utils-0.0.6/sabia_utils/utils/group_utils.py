import logging
import os
from alei_utils import adapt_logger
from utils.parquet_utils import take_files_from_path

logging.basicConfig("DEBUG")
logger = logging.getLogger(__name__)

adapter = adapt_logger(logger, {
    "servico": "IJ",
    "modulo": "IJ_AGRUPADOR_UTILS"
    })


def diff_list(PATH_TST, PATH_SABIA):
    try:
        parquet_files_tst = take_files_from_path(PATH_TST)
        parquet_files_sabia = take_files_from_path(PATH_SABIA)
        adapter.debug(
            f"Arquivo tst encontrado: {parquet_files_tst}",
            evento_status="E_S",
            tag_evento="ARQUIVO TST ENCONTRADO"
        )
        adapter.debug(
            f"Arquivo sabia encontrado: {parquet_files_sabia}",
            evento_status="E_S",
            tag_evento="ARQUIVO SABIA ENCONTRADO"
        )

        list_tst = [
            os.path.basename(file)
            for file in parquet_files_tst if file.endswith('.parquet')
            ]
        list_sabia = [
            os.path.basename(file)
            for file in parquet_files_sabia if file.endswith('.parquet')
            ]
        adapter.debug(
            "busca de diferenças entre listas",
            evento_status="E_S",
            tag_evento="BUSCA DE DIFERENÇAS ENTRE LISTAS"
        )
        return list(set(list_tst) - set(list_sabia))
    except Exception as error:
        adapter.error(
            f"erro ao buscar diferenças entre listas: {error}",
            evento_status="E_E",
            tag_evento="ERRO AO BUSCAR DIFERENÇAS ENTRE LISTAS"
        )
        return None


def same_list(PATH_TST, PATH_SABIA):
    try:
        parquet_files_tst = take_files_from_path(PATH_TST)
        parquet_files_sabia = take_files_from_path(PATH_SABIA)
        adapter.debug(
            f"Arquivo tst encontrado: {parquet_files_tst}",
            evento_status="E_S",
            tag_evento="ARQUIVO TST ENCONTRADO"
        )
        adapter.debug(
            f"Arquivo sabia encontrado: {parquet_files_sabia}",
            evento_status="E_S",
            tag_evento="ARQUIVO SABIA ENCONTRADO"
        )

        list_tst = [
            os.path.basename(file)
            for file in parquet_files_tst if file.endswith('.parquet')
            ]
        list_sabia = [
            os.path.basename(file)
            for file in parquet_files_sabia if file.endswith('.parquet')
            ]
        adapter.debug(
            "busca de semelhanças entre listas",
            evento_status="E_S",
            tag_evento="BUSCA DE SEMELHANÇAS ENTRE LISTAS"
        )
        return list(set(list_tst) & set(list_sabia))
    except Exception as error:
        adapter.error(
            f"erro ao buscar semelhanças entre listas: {error}",
            evento_status="E_E",
            tag_evento="ERRO AO BUSCAR SEMELHANÇAS ENTRE LISTAS"
        )
        return None