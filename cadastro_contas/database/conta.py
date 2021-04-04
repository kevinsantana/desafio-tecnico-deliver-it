from cadastro_contas.database import campos_obrigatorios, DataBase


class Conta(DataBase):
    def __init__(self, id_conta: int = None, nome: str = None, valor_original: float = None,
                 data_vencimento: str = None, data_pagamento: str = None):
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
        :param str data_vencimento: Data de vencimento da conta, no formato aceito
            pelo postgres yyyy-mm-dd.
        :param str data_pagamento: Data de pagamento da conta, no formato aceito
            pelo postgres yyyy-mm-dd.
        :return: True se a operação for exeutada com sucesso, False caso contrário.
        :rtype: bool
        """
        self.query_string = """INSERT INTO CONTA (NOME, VALOR_ORIGINAL, DATA_VENCIMENTO, DATA_PAGAMENTO)
            VALUES (%(nome)s, %(valor_original)s, %(data_vencimento)s, %(data_pagamento)s)"""
        return True if self.insert() else False

    @campos_obrigatorios(["id_conta"])
    def atualizar(self):
        """
        Atualiza uma conta.

        :param int id_conta: Identificador da conta a ser atualizada.
        :param str nome: Titular da conta.
        :param float valor_original: Valor monetário da conta, sem juros.
        :param str data_vencimento: Data de vencimento da conta, no formato aceito
            pelo postgres yyyy-mm-dd.
        :param str data_pagamento: Data de pagamento da conta, no formato aceito
            pelo postgres yyyy-mm-dd.
        :return: True se a operação for exeutada com sucesso, False caso contrário.
        :rtype: bool
        """
        self.query_string = ""
        if self.__nome:
            self.query_string = "UPDATE CONTA SET NOME = %(nome)s"
        if self.__valor_orignal:
            self.query_string = "UPDATE CONTA SET VALOR_ORIGINAL = %(valor_original)s"
        if self.__data_vencimento:
            self.query_string = "UPDATE CONTA SET DATA_VENCIMENTO = %(data_vencimento)s"
        if self.__data_pagamento:
            self.query_string = "UPDATE CONTA SET DATA_PAGAMENTO = %(data_pagamento)s"
        self.query_string += " WHERE CONTA.ID_CONTA = %(id_conta)s"
        return True if self.insert() else False

    @campos_obrigatorios(["id_conta", "nome"])
    def existe(self):
        """
        Verifica se uma conta existe no banco de dados.

        :param int id_conta: Identificador da conta.
        :param str nome: Titular da conta.
        :return: True se a conta for encontrada, False caso contrário.
        :rtype: bool
        """
        self.query_string = ""
        if self.__id_conta:
            self.query_string = "SELECT COUNT(*) FROM CONTA WHERE CONTA.ID_CONTA = %(id_conta)s"
        if self.__nome:
            self.query_string = "SELECT COUNT(*) FROM CONTA WHERE CONTA.NOME = %(nome)s"
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
                 valor_corrigido: float = None, data_vencimento: str = None,
                 dias_atraso: int = None, data_pagamento: str = None):
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
    def listar_contas_titular(self) -> list:
        """
        Lista as contas de um usuário.

        :param str nome: Titular da conta.
        :return: Lista de objetos :class:`database.conta.Conta`, em que cada
            objeto é uma conta atribuída ao titular encontrado no banco de dados.
        :rtype: list
        """
        self.query_string = "SELECT * FROM CONTA WHERE CONTA.NOME = %(nome)s"
        return [ListarContas(**dict(conta)) for conta in self.find_all()]

    def listar_todos(self, quantidade: int, pagina: int):
        """
        Lista todas as contas da base, paginando o resultado.

        :param int quantidade: Quantidade de registros por bloco de paginação.
        :param int pagina: Bloco (página) da paginação.
        :return: Total de contas e contas a pagar da base e lista de objetos
            :class:`database.conta.Conta`, em que cada objeto é uma conta encontrada
            no banco de dados.
        :rtype: tuple
        """
        self.__offset = (pagina-1)*quantidade
        self.__quantidade = quantidade
        self.query_string = "SELECT * FROM CONTA LIMIT %(quantidade)s OFFSET %(offset)s"
        contas, total = self.find_all(total=True)
        return total, [ListarContas(**dict(conta)) for conta in contas]
