from cadastro_contas.database.juros import Juros
from cadastro_contas.excecoes.conta import DataInvalidaException


def calcular_juros(*, dias_em_atraso: int, valor_original: int):
    """
    Calcula o valor corrigido com juros de uma conta em atraso.

    :param int dias_em_atraso: Quantidade de dias que a conta está atrasada.
    :param int valor_original: Valor original da conta.
    :raises DataInvalidaException: Se a data informada for inválida, isto é, não
        existe regra para a quantidade de dias em atraso ou não é do tipo inteiro.
    :return: Valor da conta em atraso.
    :rtype: float
    """
    valor_corrigido = 0.0
    if dias_em_atraso >= 1 and type(dias_em_atraso) is int:
        regra = Juros(dias_em_atraso=dias_em_atraso).juros_por_dia()
        valor_corrigido = (valor_original * regra.porcentagem_multa/100) + \
                          ((dias_em_atraso * regra.juros_por_dia) * valor_original) + valor_original
        return "R${:,.2f}".format(valor_corrigido)
    else:
        raise DataInvalidaException(dias_em_atraso)


def inserir():
    pass


def consultar_juros(*, dias_em_atraso: int):
    pass
