from datetime import datetime
from collections import defaultdict

from cadastro_contas.modulos.juros import calcular_juros
from cadastro_contas.database.conta import Conta, ListarContas
from cadastro_contas.modulos.utils import data_e_valida, data_to_postgres_data, postges_data_to_data
from cadastro_contas.excecoes.conta import (
    ContaInexistenteException, DataInvalidaException, DataVencimentoMaiorDataPagamentoException,
    TitularInexistenteException
    )


def __montar_conta(conta) -> dict:
    """
    Formata conta para apresentação. Calculando dias em atraso e valor corrigido.

    :param conta: Conta a ser formatada.
    :return: Dicionário da conta formatada.
    :rtype: list
    """
    data_vencimento, data_pagamento = postges_data_to_data(conta.data_vencimento), postges_data_to_data(conta.data_pagamento) # noqa
    dias_atrasados = dias_atraso(data_vencimento=data_vencimento, data_pagamento=data_pagamento)
    return {
        "nome": conta.nome,
        "valor_original": "R${:,.2f}".format(conta.valor_original),
        "dias_atraso": dias_atrasados,
        "valor_corrigido": calcular_juros(dias_em_atraso=dias_atrasados,
                                          valor_original=conta.valor_original)
        if dias_atrasados >= 1 else conta.valor_original,
        "data_vencimento": data_vencimento,
        "data_pagamento": data_pagamento
    }


def dias_atraso(*, data_vencimento: str, data_pagamento: str) -> int:
    """
    Calcula a quantidade de dias que uma conta está atrasada.

    :param str data_vencimento: Data de vencimento da conta, no formato dd/mm/yyyy.
    :param str data_pagamento: Data de pagamento da conta, no formato dd/mm/yyyy.
    :raises DataVencimentoMaiorDataPagamentoException: Se a data de vencimento for maior que a data de pagamento.
    :raises DataInvalidaException: Se uma das duas datas tiver um formato inválido.
    :return: Quantidade de dias que a conta está em atraso.
    :rtype: int
    """
    if data_vencimento > data_pagamento:
        raise DataVencimentoMaiorDataPagamentoException(data_vencimento=data_vencimento, data_pagamento=data_pagamento)
    if data_e_valida(data_vencimento):
        if data_e_valida(data_pagamento):
            d1 = datetime.strptime(data_vencimento, "%d/%m/%Y").date()
            d2 = datetime.strptime(data_pagamento, "%d/%m/%Y").date()
            return (d2 - d1).days
        else:
            raise DataInvalidaException(data=data_pagamento)
    else:
        raise DataInvalidaException(data=data_vencimento)


def inserir(*, nome: str, valor_original: float, data_vencimento: str,
            data_pagamento: str):
    """
    Insere uma conta no banco de dados.

    :param str nome: Titular da conta.
    :param float valor_original: Valor monetário da conta, sem juros.
    :param str data_vencimento: Data de vencimento da conta, no formato dd/mm/yyyy.
    :param str data_pagamento: Data de pagamento da conta, no formato dd/mm/yyyy.
    :raises DataVencimentoMaiorDataPagamentoException: Se a data de vencimento for maior que a data de pagamento.
    :return: True se a operação for exeutada com sucesso, False caso contrário.
    :rtype: bool
    """
    data_vencimento, data_pagamento = data_to_postgres_data(data_vencimento), data_to_postgres_data(data_pagamento)
    if data_vencimento > data_pagamento:
        raise DataVencimentoMaiorDataPagamentoException(data_vencimento=data_vencimento,
                                                        data_pagamento=data_pagamento)
    insercao = Conta(nome=nome, valor_original=valor_original, data_vencimento=data_vencimento,
                     data_pagamento=data_pagamento).inserir()
    return True if insercao else False


def atualizar(*, id_conta: int, nome: str = None, valor_original: float = None,
              data_vencimento: str = None, data_pagamento: str = None):
    """
    Atualiza as informações de uma conta no banco de dados.

    :param int id_conta: Identificador da conta a ser atulizada.
    :param str nome: Titular da conta.
    :param float valor_original: Valor monetário da conta.
    :param str data_vencimento: Data de vencimento da conta, no formato dd/mm/yyyy
    :param str data_pagamento: Data de pagamento da conta, no formato dd/mm/yyyy
    :raises ContaInexistenteException: Se a conta informada não for encontrada no banco de dados.
    :raises DataVencimentoMaiorDataPagamentoException: Se a data de vencimento for maior que a data de pagamento.
    :return: True se a conta tiver sido atualizado com sucesso, False caso contrário.
    :rtype: bool
    """
    if Conta(id_conta=id_conta).existe():
        if data_vencimento:
            data_vencimento = data_to_postgres_data(data_vencimento)
        if data_pagamento:
            data_pagamento = data_to_postgres_data(data_pagamento)
        if data_pagamento and data_vencimento:
            if data_vencimento > data_pagamento:
                raise DataVencimentoMaiorDataPagamentoException(data_vencimento=data_vencimento,
                                                                data_pagamento=data_pagamento)
        return Conta(id_conta=id_conta, nome=nome, valor_original=valor_original,
                     data_vencimento=data_vencimento, data_pagamento=data_pagamento).atualizar()
    else:
        raise ContaInexistenteException(404, id_conta)


def deletar(*, id_conta: int):
    """
    Excluí uma conta do banco de dados.

    :param int id_conta: Identificador da conta.
    :raises ContaInexistenteException: Se a conta informada não for encontrada no banco de dados.
    :return: True se a operação for executada com sucesso, False caso contrário.
    :rtype: bool
    """
    if Conta(id_conta=id_conta).existe():
        return Conta(id_conta=id_conta).deletar()
    else:
        raise ContaInexistenteException(404, id_conta)


def listar_contas_titular(*, nome: str) -> list:
    """
    Lista todas as contas de um usuário, a partir do seu nome.

    :param str nome: Titular da(s) conta(s).
    :raises TitularInexistenteException: Se o titular da conta informada não existir.
    :return: Contas do titular informado.
    :rtype: list
    """
    if Conta(nome=nome).existe():
        return [__montar_conta(conta) for conta in ListarContas(nome=nome).listar_contas_titular()]
    else:
        raise TitularInexistenteException(404, nome)


def listar_todos(quantidade: int, pagina: int) -> dict:
    """
    separar as contas por titular, devolvendo o resultado em ordem alfabetica
    Retorna todas as contas disponibilizadas no banco de dados, paginando o resultado.

    :param int quantidade: Quantidade de registros por bloco de paginação.
    :param int pagina: Bloco (página) da paginação.
    :return: Dicionário ordenado por titular de todas as contas disponíveis no
        banco de dados.
    :rtpe: dict
    """
    contas_titulares = defaultdict(list)
    total, contas = ListarContas().listar_todos(quantidade=quantidade, pagina=pagina)
    return total, [contas_titulares[conta.nome].append(__montar_conta(conta)) for conta in contas]
