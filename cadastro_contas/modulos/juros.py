from cadastro_contas.database.juros import Juros
from cadastro_contas.excecoes.conta import DataInvalidaException
from cadastro_contas.excecoes.juros import JurosInexistenteException


def calcular_juros(*, dias_em_atraso: int, valor_original: int):
    """
    Calcula o valor corrigido com juros de uma conta em atraso.

    :param int dias_em_atraso: Quantidade de dias que a conta está atrasada.
    :param int valor_original: Valor original da conta.
    :return: Valor da conta em atraso.
    :rtype: float
    """
    valor_corrigido = 0.0
    regra = consultar_juros(dias_em_atraso=dias_em_atraso)
    valor_corrigido = (valor_original * regra.porcentagem_multa/100) + \
                      ((dias_em_atraso * regra.juros_por_dia) * valor_original) + valor_original
    return "R${:,.2f}".format(valor_corrigido)


def inserir(*, dias_em_atraso: int, porcentagem_multa: int, juros_por_dia: float):
    """
    Inserir uma nova regra de juros no banco de dados.

    :param int dias_em_atraso: Quantidade de dias em atraso nos quais a regra se aplica.
    :param int porcentagem_multa: Porcentagem inteira de juros aplicáveis.
    :param float juros_por_dia: Porcentagem de juros aplicáveis por dia de atraso.
    :return: True se a operação for exeutada com sucesso, False caso contrário.
    :rtype: bool
    """
    return Juros(dias_em_atraso=dias_em_atraso, porcentagem_multa=porcentagem_multa,
                 juros_por_dia=juros_por_dia).inserir()


def atualizar(*, id_juros: int, dias_em_atraso: int = None, porcentagem_multa: int = None,
              juros_por_dia: float = None):
    """
    Atualiza uma regra de juros no banco de dados.

    :param int id_juros: Identificador no banco de dados do juros.
    :param int dias_em_atraso: Quantidade de dias em atraso nos quais a regra se aplica.
    :param int porcentagem_multa: Porcentagem inteira de juros aplicáveis.
    :param float juros_por_dia: Porcentagem de juros aplicáveis por dia de atraso.
    :raises JurosInexistenteException: Se o juros não existir.
    :return: True se a operação for exeutada com sucesso, False caso contrário.
    :rtype: bool
    """
    if Juros(id_juros=id_juros).buscar():
        return Juros(id_juros, dias_em_atraso, porcentagem_multa, juros_por_dia).atualizar()
    else:
        raise JurosInexistenteException(404, id_juros)


def deletar(*, id_juros: int):
    """
    Deleta uma regra de juros do banco de dados.

    :param int id_juros: Identificador no banco de dados do juros.
    :raises JurosInexistenteException: Se o juros não existir.
    :return: True se a operação for exeutada com sucesso, False caso contrário.
    :rtype: bool
    """
    if Juros(id_juros=id_juros).buscar():
        return Juros(id_juros=id_juros).deletar()
    else:
        raise JurosInexistenteException(404, id_juros)


def consultar_juros(*, dias_em_atraso: int):
    """
    Retorna a regra de juros para a quantidade de juros em atraso.

    :param int dias_em_atraso: Quantidade de dias que a conta está atrasada.
    :raises DataInvalidaException: Se a data informada for inválida, isto é, não
        existe regra para a quantidade de dias em atraso ou não é do tipo inteiro.
    """
    if dias_em_atraso >= 1 and type(dias_em_atraso) is int:
        regra_dias = {
            3: 3 if dias_em_atraso >= 1 and dias_em_atraso <= 3 else None,
            4: 4 if dias_em_atraso >= 4 and dias_em_atraso <= 5 else None,
            6: 6 if dias_em_atraso >= 6 else None
        }
        return Juros(dias_em_atraso=[regra for regra in regra_dias.values() if regra][0]).consultar_regra()
    else:
        raise DataInvalidaException(dias_em_atraso)


def listar():
    """
    Lista as regras de juros do banco de dados.

    :return: Lista de objeto :class:`database.juros.Juros` ou None
    :rtype: list
    """
    return [juros.dict() for juros in Juros().listar()]
