from alei_utils import adapt_logger
from utils.group_utils import diff_list, same_list
from concat import concatenate_files

import logging
import timeit
import shutil

logging.basicConfig('DEBUG')
logger = logging.getLogger(__name__)

adapter = adapt_logger(logger, {
    "servico": "IJ",
    "modulo": "IJ_AGRUPADOR_GROUPER"
    })


def copy_new_files(PATH_TST, PATH_SABIA):
    '''
    Copia do path TST para o path SABIA os arquivos que não existem no path SABIA
    :param PATH_TST: path de origem dos arquivos
    :param PATH_SABIA: path de destino dos arquivos
    :return: None
    '''
    try:
        inicio = timeit.default_timer()
        diff_files = diff_list(PATH_TST, PATH_SABIA)
        if bool(diff_files):
            adapter.info(
                f'''arquivos diferentes: {
                    diff_files
                    }''',
                evento_status="E_S",
                tag_evento="ARQUIVOS DIFERENTES"
                )
            adapter.debug(
                "copia de arquivos iniciada",
                evento_status="E_S",
                tag_evento="COPIA INICIADA"
            )
            for file in diff_files:
                shutil.copy(f'{PATH_TST}/{file}', PATH_SABIA)
                adapter.debug(
                    f'arquivo copiado: {file}',
                    evento_status="E_S",
                    tag_evento="ARQUIVO COPIADO"
                )
            fim = timeit.default_timer()
            tempo = fim-inicio
            adapter.debug(
                f"tempo de agrupamento: {round(round(tempo,2)/60,2)} minutos",
                evento_status="E_S",
                tag_evento="TEMPO DE EXECUCAO"
            )
            adapter.info(
                "copia finalizada",
                evento_status="E_S",
                tag_evento="COPIA FINALIZADA"
            )
        else:
            adapter.debug(
                "nenhum arquivo diferente encontrado",
                evento_status="E_S",
                tag_evento="PATHS SEM DIFERENÇAS"
            )

    except Exception as erro:
        adapter.error(
            f"Erro ao agrupar os arquivos: {erro}",
            evento_status="E_E",
            tag_evento="AGRUPAMENTO ENCERRADO COM ERRO"
        )


def process_existent_files(PATH_TST, PATH_SABIA):
    '''
    Agrupa os arquivos que existem nos dois paths
    :param PATH_TST: path de origem dos arquivos
    :param PATH_SABIA: path de destino dos arquivos
    :return: None
    '''
    try:
        same_files = same_list(PATH_TST, PATH_SABIA)
        if bool(same_files):
            inicio = timeit.default_timer()
            adapter.info(
                "agrupamento iniciado de arquivos existentes",
                evento_status="E_S",
                tag_evento="AGRUPAMENTO INICIADO"
            )
            for file in same_files:
                PATH_TST = f'{PATH_TST}/{file}'
                PATH_SABIA = f'{PATH_SABIA}/{file}'
                concatenate_files([PATH_TST,PATH_SABIA], PATH_SABIA, file)
            fim = timeit.default_timer()
            tempo = fim-inicio
            adapter.debug(
                f"tempo de agrupamento: {round(round(tempo,2)/60,2)} minutos",
                evento_status="E_S",
                tag_evento="TEMPO DE EXECUCAO"
            )
            adapter.info(
                "agrupamento finalizado",
                evento_status="E_S",
                tag_evento="AGRUPAMENTO FINALIZADO"
            )
        else:
            adapter.debug(
                "nenhum arquivo semelhante foi encontrado",
                evento_status="E_S",
                tag_evento="PATHS SEM DIFERENÇAS"
            )
    except Exception as error:
        adapter.error(
            f"Erro ao agrupar os arquivos: {error}",
            evento_status="E_E",
            tag_evento="AGRUPAMENTO ENCERRADO COM ERRO"
        )


def process_all_files(PATH_TST, PATH_SABIA):
    '''
    Agrupa todos os arquivos dos paths
    :param PATH_TST: path de origem dos arquivos
    :param PATH_SABIA: path de destino dos arquivos
    :return: None
    '''
    try:
        inicio = timeit.default_timer()
        adapter.info(
            "agrupamento geral iniciado",
            evento_status="E_S",
            tag_evento="AGRUPAMENTO INICIADO"
        )
        copy_new_files(PATH_TST, PATH_SABIA)
        process_existent_files(PATH_TST, PATH_SABIA)
        fim = timeit.default_timer()
        tempo = fim-inicio
        adapter.debug(
            f"tempo de agrupamento: {round(round(tempo,2)/60,2)} minutos",
            evento_status="E_S",
            tag_evento="TEMPO DE EXECUCAO"
        )
        adapter.info(
            "agrupamento finalizado",
            evento_status="E_S",
            tag_evento="AGRUPAMENTO FINALIZADO"
        )
    except Exception as error:
        adapter.error(
            f"Erro ao agrupar os arquivos: {error}",
            evento_status="E_E",
            tag_evento="AGRUPAMENTO ENCERRADO COM ERRO"
        )
