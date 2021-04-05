from cadastro_contas.excecoes import CadastroContasException


class JurosInexistenteException(CadastroContasException):
    def __init__(self, status_code: int, id_juros: int = None):
        self.status_code = status_code
        self.message = f"A regra de juros {id_juros} não existe"
        super().__init__(self.status_code, self.message)
