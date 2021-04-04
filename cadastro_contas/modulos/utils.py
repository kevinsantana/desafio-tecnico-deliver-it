import re
from datetime import datetime

from cadastro_contas.config import VALIDA_DATA_RE
from cadastro_contas.excecoes.conta import DataInvalidaException


def data_e_valida(data: str) -> bool:
    return True if re.compile(VALIDA_DATA_RE).search(data) else False


def converter_data(data: str, timestamp: bool = False):
    if data_e_valida(data):
        return datetime.strptime(data, "%d/%m/%Y").timestamp() if timestamp else datetime.strptime(data, '%d/%m/%Y').date() # noqa
    else:
        raise DataInvalidaException(data=data)


def timestamp_to_data(data: float):
    return datetime.fromtimestamp(data).strftime("%d/%m/%Y")
