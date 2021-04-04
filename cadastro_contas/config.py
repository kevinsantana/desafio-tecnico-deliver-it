import os


PGSQL_DB = os.environ.get("PGSQL_DB", "contas")
PGSQL_HOST = os.environ.get("PGSQL_HOST", "db_cadastro_contas")
PGSQL_PASS = os.environ.get("PGSQL_PASS", "contas")
PGSQL_USR = os.environ.get("PGSQL_USR", "contas")
PGSQL_PORT = os.environ.get("PGSQL_PORT", "5432")

VALIDA_DATA_RE = r'^([0-2][0-9]|(3)[0-1])(\/)(((0)[0-9])|((1)[0-2]))(\/)\d{4}$'
