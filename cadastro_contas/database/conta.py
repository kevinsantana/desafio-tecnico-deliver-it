from cadastro_contas.database import campos_obrigatorios, DataBase


class Conta(DataBase):
    def __init__(self, id_conta: int = None, nome: str = None, valor_original: float = None,
                 data_vencimento: float = None, data_pagamento: float = None):
        self.__id_conta = id_conta
        self.__nome = nome
        self.__valor_original = valor_original
        self.__data_vencimento = data_vencimento
        self.__data_pagamento = data_pagamento

    @property
    def id_conta(self):
        return self.__id_conta

    @property
    def nome(self):
        return self.__nome

    @property
    def valor_original(self):
        return self.__valor_orignal

    @property
    def data_vencimento(self):
        return self.__data_vencimento

    @property
    def data_pagamento(self):
        return self.__data_pagamento

    def dict(self):
        return {key.replace("_Conta__", ""): value for key, value in self.__dict__.items()}

    @campos_obrigatorios(["nome", "valor_original", "data_vencimento", "data_pagamento"])
    def inserir(self):
        """
        Insere uma conta no banco de dados.

        :param str nome: Titular da conta.
        :param float valor_original: Valor monetário da conta, sem juros.
        :param float data_vencimento: Timestamp da data de vencimento da conta.
        :param float data_pagamento: Timestamp da data de pagamento da conta
        :return: True se a operação for exeutada com sucesso, False caso contrário.
        :rtype: bool
        """
        self.query_string = """INSERT INTO CONTA (NOME, VALOR_ORIGINAL, DATA_VENCIMENTO, DATA_PAGAMENTO)
            VALUES (%(nome)s, %(valor_original)s, to_timestamp(%(data_vencimento)s, 'YYYY-MM-DD'),
            to_timestamp(%(data_pagamento)s, 'YYYY-MM-DD'))"""
        return True if self.insert() else False

    @campos_obrigatorios(["id_conta"])
    def atualizar(self):
        """
        Atualiza uma conta.

        :param int id_conta: Identificador da conta a ser atualizada.
        :param str nome: Titular da conta.
        :param float valor_original: Valor monetário da conta, sem juros.
        :param float data_vencimento: Timestamp da data de vencimento da conta.
        :param float data_pagamento: Timestamp da data de pagamento da conta
        :return: True se a operação for exeutada com sucesso, False caso contrário.
        :rtype: bool
        """
        self.query_string = ""
        if self.__nome:
            self.query_string = "UPDATE CONTA SET NOME = %(nome)s"
        if self.__valor_orignal:
            self.query_string = "UPDATE CONTA SET VALOR_ORIGINAL = %(valor_original)s"
        if self.__data_vencimento:
            self.query_string = "UPDATE CONTA SET DATA_VENCIMENTO = to_timestamp(%(data_vencimento)s, 'YYYY-MM-DD')"
        if self.__data_pagamento:
            self.query_string = "UPDATE CONTA SET DATA_PAGAMENTO = to_timestamp(%(data_pagamento)s, 'YYYY-MM-DD')"
        self.query_string += " WHERE CONTA.ID_CONTA = %(id_conta)s"
        return True if self.insert() else False

    @campos_obrigatorios(["id_conta"])
    def existe(self):
        """
        Verifica se uma conta existe no banco de dados.

        :param int id_conta: Identificador da conta.
        :return: True se a conta for encontrada, False caso contrário.
        :rtype: bool
        """
        self.query_string = "SELECT COUNT(*) FROM CONTA WHERE CONTA.ID_CONTA = %(id_conta)s"
        return True if self.find_one()[0] else False

    @campos_obrigatorios(["id_conta"])
    def deletar(self):
        """
        Deleta uma conta do banco de dados.

        :param int id_conta: Identificador da conta.
        :return: True se a operação for exeutada com sucesso, False caso contrário.
        :rtype: bool
        """
        self.query_string = "DELETE FROM CONTA WHERE CONTA.ID_CONTA = %(id_conta)s"
        return True if self.insert() else False


class ListarContas(DataBase):
    def __init__(self, id_conta: int = None, nome: str = None, valor_original: float = None,
                 valor_corrigido: float = None, data_vencimento: float = None,
                 dias_atraso: int = None, data_pagamento: float = None):
        self.__id_conta = id_conta
        self.__nome = nome
        self.__valor_original = valor_original
        self.__valor_corrigido = valor_corrigido
        self.__dias_atraso = dias_atraso
        self.__data_vencimento = data_vencimento
        self.__data_pagamento = data_pagamento

    @property
    def id_conta(self):
        return self.__id_conta

    @property
    def nome(self):
        return self.__nome

    @property
    def valor_original(self):
        return self.__valor_orignal

    @property
    def valor_corrigido(self):
        return self.__valor_corrigido

    @property
    def dias_atraso(self):
        return self.__dias_atraso

    @property
    def data_vencimento(self):
        return self.__data_vencimento

    @property
    def data_pagamento(self):
        return self.__data_pagamento

    def dict(self):
        return {key.replace("_ListarContas__", ""): value for key, value in self.__dict__.items()}

    @campos_obrigatorios(["nome"])
    def listar_um(self) -> list:
        """
        Lista as contas de um usuário.

        :param str nome: Titular da conta.
        :return: Contas atribuídas ao usuário
        :rtype: list
        """
        self.query_string = "SELECT * FROM CONTA WHERE CONTA.NOME = %(nome)s"
        return [ListarContas(**dict(conta)) for conta in self.find_all()]

    def listar_todos(self, pagina: int, quantidade: int):
        """
        Lista todas as contas da base.

        :param int quantidade: Quantidade de registros por bloco de paginação.
        :param int pagina: Bloco (página) da paginação.
        :return: Total de contas e contas a pagar da base.
        :rtype: tuple
        """
        self.__offset = (pagina-1)*quantidade
        self.__quantidade = quantidade
        self.query_string = "SELECT * FROM CONTA LIMIT %(quantidade)s OFFSET %(offset)s"
        contas, total = self.find_all(total=True)
        return total, [ListarContas(**dict(conta)) for conta in contas]
