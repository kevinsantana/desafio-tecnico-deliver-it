import abc
import functools

import psycopg2
from loguru import logger
from psycopg2 import OperationalError
from psycopg2.extras import DictCursor

from cadastro_contas.excecoes import CampoObrigatorioException
from cadastro_contas.config import (
    PGSQL_DB, PGSQL_HOST, PGSQL_PASS, PGSQL_PORT, PGSQL_USR,
)


def campos_obrigatorios(campos):
    """
    Decorator utilizado nos métodos do banco de dados, garante que, para uma
    determinada transação (DDL ou DML), os campos solicitados sejam informados,
    caso contrário uma exceção é lançada.
    :param campos: Campo(s) necessário(s) para a transação.
    :raises CampoObrigatorioException: Se algum do(s) campo(s) obrigatório(s) não
        for(em) informado(s).
    """
    def decorator_campos_obrigatorios(func):
        @functools.wraps(func)
        def wrapper_campos_obrigatorios(self, *args, **kwargs):
            for campo in campos:
                if self.dict().get(campo) is None:
                    raise CampoObrigatorioException(self.__class__.__name__, campo)
            return func(self, *args, **kwargs)
        return wrapper_campos_obrigatorios
    return decorator_campos_obrigatorios


class DataBase():
    """
    Cada tabela do banco de dados é uma classe, em que cada coluna é um atributo
    da classe e os métodos são suas transações (DML ou DDL). Os dados devolvidos
    de operações com o banco de dados são dicionários (cursor_factory=DictCursor)
    em que cada chave é a coluna da tabela e o valor desta chave é o resultado da
    operação, para isto, todas as classes que herdam de DataBase precisam implementar
    o seu método dict.
    Assim, é possível instanciar um objeto da classe, ou seja, uma tabela do banco
    de dados mapeando cada atributo da classe a uma coluna desta tabela. E, ainda,
    aproveitando da OO não é necessário que as demais classes implemetem as transações
    comuns a todas as tabelas do banco de dados: insert, find_one, find_all.
    """
    def __connect(self):
        """
        Efetua a conexão com o banco de dados, os dados de conexão são capturados
        de variáveis de ambientes exportadas no arquivo /cadastro_contas/config.py.
        :raises OperationalError: Se não for possível a conexão com o banco de dados.
        """
        try:
            self.__connection = psycopg2.connect(user=PGSQL_USR,
                                                 password=PGSQL_PASS,
                                                 host=PGSQL_HOST,
                                                 port=PGSQL_PORT,
                                                 database=PGSQL_DB)
            self.__cursor = self.__connection.cursor(cursor_factory=DictCursor)
        except OperationalError as op_error:
            logger.debug(f'Falha de conexao: {op_error}')

    def __disconect(self):
        """
        Fecha a conexão com o banco de dados.
        """
        self.__cursor.close()
        self.__connection.close()

    def insert(self):
        """
        Insere um dado no banco de dados. As classes que herdam de DataBase devem
        ser instanciadas com o método query_string que é a operação que será
        executada no banco de dados, quando assim for necessário, e o método dict
        para que os valores do objeto instanciado sejam mapeados na transação com
        o banco de dados, da seguinte maneira:

        .. code-block:: python

            self.__cursor.execute('''
                        INSERT INTO some_table (an_int, a_date, another_date, a_string)
                        VALUES (%(int)s, %(date)s, %(date)s, %(str)s);
                        ''',
                        {'int': 10, 'str': "O'Reilly", 'date': datetime.date(2005, 11, 18)})

        A conexão é imediatamente aberta e logo em seguida fechada, garantindo que
        a conexão não fique aberta desnecessariamente.
        :return: Quantidade de linhas afetadas pela operação, em caso de sucesso 1
        senão None, isto é, a operação não foi bem sucedida.
        :rtype: int ou None
        """
        self.__connect()
        self.__cursor.execute(self.query_string, self.dict())
        self.__connection.commit()
        result = self.__cursor.rowcount
        self.__disconect()
        return result

    def find_one(self):
        """
        Trás (fetch) a próxima linha do banco de dados afetadas pela consulta
        construída em query_string. Caso não exista registro é retornado None.
        A conexão é imediatamente aberta e logo em seguida fechada, garantindo que
        não fique aberta desnecessariamente.
        :return: Resultado da busca.
        :rtype: dict
        """
        self.__connect()
        self.__cursor.execute(self.query_string, self.dict())
        result = self.__cursor.fetchone()
        self.__disconect()
        return result

    def find_all(self, total=False) -> list:
        """
        Trás (fetch) todas as linhas do banco de dados afetadas pela consulta
        construída em query_string. Caso não exista registro é retornado uma lista vazia.
        A conexão é imediatamente aberta e logo em seguida fechada, garantindo que
        a conexão fique aberta desnecessariamente.
        :param bool total: Caso seja necessário retornar a quantidade total de
        registros da busca.
        :return: Resultado da busca.
        :rtype: list
        """
        self.__connect()
        self.__cursor.execute(self.query_string, self.dict())
        result = self.__cursor.fetchall()
        self.__disconect()
        if total:
            return result, self.__cursor.rowcount
        return result

    @abc.abstractclassmethod
    def dict(self):
        raise NotImplementedError
