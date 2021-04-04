from cadastro_contas.excecoes import CadastroContasException


class ContaInexistenteException(CadastroContasException):
    def __init__(self, status_code: int, id_conta: int = None):
        self.status_code = status_code
        self.message = f"O id {id_conta} da conta não existe"
        super().__init__(self.status_code, self.message)
