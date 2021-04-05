from cadastro_contas.database import campos_obrigatorios, DataBase


class Juros(DataBase):
    def __init__(self, id_juros: int = None, dias_em_atraso: int = None,
                 porcentagem_multa: int = None, juros_por_dia: float = None):
        self.__id_juros = id_juros
        self.__dias_em_atraso = dias_em_atraso
        self.__porcentagem_multa = porcentagem_multa
        self.__juros_por_dia = juros_por_dia

    @property
    def id_juros(self):
        return self.__id_juros

    @property
    def dias_atraso(self):
        return self.__dias_em_atraso

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

    @campos_obrigatorios(["dias_em_atraso", "porcentagem_multa", "juros_por_dia"])
    def inserir(self):
        """
        Insere uma nova regra de juros no banco de dados.

        :param int dias_em_atraso: Quantidade de dias em atraso nos quais a regra se aplica.
        :param int porcentagem_multa: Porcentagem inteira de juros aplicáveis.
        :param float juros_por_dia: Porcentagem de juros aplicáveis por dia de atraso.
        :return: True se a operação for exeutada com sucesso, False caso contrário.
        :rtype: bool
        """
        self.query_string = """INSERT INTO DOMINIO_JUROS (DIAS_EM_ATRASO, PORCENTAGEM_MULTA, JUROS_POR_DIA)
            VALUES (%(dias_em_atraso)s, %(porcentagem_multa)s, %(juros_por_dia)s)"""
        return True if self.insert() else False

    @campos_obrigatorios(["id_juros"])
    def atualizar(self):
        """
        Atualiza uma regra de juros no banco de dados.

        :param int id_juros: Identificador no banco de dados do juros.
        :param int dias_em_atraso: Quantidade de dias em atraso nos quais a regra se aplica.
        :param int porcentagem_multa: Porcentagem inteira de juros aplicáveis.
        :param float juros_por_dia: Porcentagem de juros aplicáveis por dia de atraso.
        :return: True se a operação for exeutada com sucesso, False caso contrário.
        :rtype: bool
        """
        self.query_string = ""
        if self.__dias_em_atraso:
            self.query_string = "UPDATE DOMINIO_JUROS SET DIAS_EM_ATRASO = %(dias_em_atraso)s"
        if self.__porcentagem_multa:
            self.query_string = "UPDATE DOMINIO_JUROS SET PORCENTAGEM_MULTA = %(porcentagem_multa)s"
        if self.__juros_por_dia:
            self.query_string = "UPDATE DOMINIO_JUROS SET JUROS_POR_DIA = %(juros_por_dia)s"
        self.query_string += " WHERE DOMINIO_JUROS.ID_JUROS = %(id_juros)s"
        return True if self.insert() else False

    @campos_obrigatorios(["id_juros"])
    def deletar(self):
        """
        Deleta uma regra de juros do banco de dados.

        :param int id_juros: Identificador no banco de dados do juros.
        :return: True se a operação for exeutada com sucesso, False caso contrário.
        :rtype: bool
        """
        self.query_string = "DELETE FROM DOMINIO_JUROS WHERE DOMINIO_JUROS.ID_JUROS = %(id_juros)s"
        return True if self.insert() else False

    @campos_obrigatorios(["id_juros"])
    def buscar(self):
        """
        Busca uma regra de juros no banco de dados.

        :param int id_juros: Identificador no banco de dados do juros.
        :return: Regra de juros do identificador informado.
        :rtype: objeto :class:`database.juros.Juros` ou None
        """
        self.query_string = "SELECT * FROM DOMINIO_JUROS WHERE DOMINIO_JUROS.ID_JUROS = %(id_juros)s"
        regra = self.find_one()
        return Juros(**dict(regra)) if regra else None

    @campos_obrigatorios(["dias_em_atraso"])
    def consultar_regra(self):
        """
        Recupera uma regra de juros do banco de dados a partir da quantidade de dias em atraso.

        :param int dias_em_atraso: Quantidade de dias em atraso nos quais a regra se aplica.
        :return: Regra de juros dos dias em atraso informado.
        :rtype: objeto :class:`database.juros.Juros` ou None
        """
        self.query_string = """SELECT DIAS_EM_ATRASO, PORCENTAGEM_MULTA, JUROS_POR_DIA
            FROM DOMINIO_JUROS WHERE DOMINIO_JUROS.DIAS_EM_ATRASO = %(dias_em_atraso)s"""
        regra = self.find_one()
        return Juros(**dict(regra)) if regra else None

    def listar(self):
        """
        Lista as regras de juros do banco de dados.

        :return: Lista de objeto :class:`database.juros.Juros` ou None
        :rtype: list
        """
        self.query_string = "SELECT * FROM DOMINIO_JUROS"
        return [Juros(**dict(regra)) for regra in self.find_all()]
