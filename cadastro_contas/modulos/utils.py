import re
from datetime import datetime

from cadastro_contas.config import VALIDA_DATA_RE
from cadastro_contas.excecoes.conta import DataInvalidaException


def data_e_valida(data: str) -> bool:
    return True if re.compile(VALIDA_DATA_RE).search(data) else False


def data_to_postgres_data(data: str, timestamp: bool = False):
    if data_e_valida(data):
        return datetime.strptime(data, '%d/%m/%Y').date()
    else:
        raise DataInvalidaException(data=data)


def postges_data_to_data(data: str):
    return datetime.strptime(data, '%Y-%m-%d').strftime('%d/%m/%Y')


def timestamp_to_data(data: float):
    return datetime.fromtimestamp(data).strftime("%d/%m/%Y")
