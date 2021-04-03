from cadastro_contas.database import campos_obrigatorios, DataBase


class Juros(DataBase):
    def __init__(self, id_juros: int = None, porcentagem_multa: int = None,
                 juros_por_dia: float = None):
        self.__id_juros = id_juros
        self.__porcentagem_multa = porcentagem_multa
        self.__juros_por_dia = juros_por_dia

    @property
    def id_juros(self):
        return self.__id_juros

    @property
    def porcentagem_multa(self):
        return self.__porcentagem_multa

    @porcentagem_multa.setter
    def porcentagem_multa(self, porcentagem_multa: int):
        if type(porcentagem_multa) is int:
            self.__porcentagem_multa = porcentagem_multa

    @property
    def juros_por_dia(self):
        return self.__juros_por_dia

    @juros_por_dia.setter
    def juros_por_dia(self, juros_por_dia: float):
        if type(juros_por_dia) is float:
            self.__juros_por_dia = juros_por_dia

    def dict(self):
        return {key.replace("_Juros__", ""): value for key, value in self.__dict__.items()}

    @campos_obrigatorios(["porcentagem_multa", "juros_por_dia"])
    def inserir(self):
        """
        Insere uma nova regra de juros no banco de dados.

        :param int porcentagem_multa: Porcentagem inteira de juros aplicáveis.
        :param float juros_por_dia: Porcentagem de juros aplicáveis por dia de atraso.
        :return: True se a operação for exeutada com sucesso, False caso contrário.
        :rtype: bool
        """
        self.query_string = """INSERT INTO JUROS (PORCENTAGEM_MULTA, JUROS_POR_DIA)
            VALUES (%(porcentagem_multa)s, %(juros_por_dia)s)"""
        return True if self.insert() else False

    @campos_obrigatorios(["id_juros"])
    def atualizar(self):
        """
        Atualiza uma regra de juros no banco de dados.

        :param int id_juros: Identificador no banco de dados do juros.
        :param int porcentagem_multa: Porcentagem inteira de juros aplicáveis.
        :param float juros_por_dia: Porcentagem de juros aplicáveis por dia de atraso.
        :return: True se a operação for exeutada com sucesso, False caso contrário.
        :rtype: bool
        """
        self.query_string = ""
        if self.__porcentagem_multa:
            self.query_string = "UPDATE JUROS SET PORCENTAGEM_MULTA = %(porcentagem_multa)s"
        if self.__juros_por_dia:
            self.query_string = "UPDATE JUROS SET JUROS_POR_DIA = %(juros_por_dia)s"
        self.query_string += " WHERE JUROS.ID_JUROS = %(id_juros)s"
        return True if self.insert() else False

    @campos_obrigatorios(["id_juros"])
    def deletar(self):
        """
        Deleta uma regra de juros do banco de dados.

        :param int id_juros: Identificador no banco de dados do juros.
        :return: True se a operação for exeutada com sucesso, False caso contrário.
        :rtype: bool
        """
        self.query_string = "DELETE FROM JUROS WHERE JUROS.ID_JUROS = %(id_juros)s"
        return True if self.insert() else False

    @campos_obrigatorios(["id_juros"])
    def buscar(self):
        """
        Busca uma regra de juros no banco de dados.

        :param int id_juros: Identificador no banco de dados do juros.
        :return: Regra de juros do identificador informado.
        :rtype: dict
        """
        self.query_string = "SELECT * FROM JUROS WHERE JUROS.ID_JUROS = %(id_juros)s"
        return self.find_one()
