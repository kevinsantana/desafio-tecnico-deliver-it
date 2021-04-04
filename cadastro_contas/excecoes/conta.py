from cadastro_contas.excecoes import CadastroContasException


class ContaInexistenteException(CadastroContasException):
    def __init__(self, status_code: int, id_conta: int = None):
        self.status_code = status_code
        self.message = f"O id {id_conta} da conta não existe"
        super().__init__(self.status_code, self.message)


class TitularInexistenteException(CadastroContasException):
    def __init__(self, status_code: int, nome: str):
        self.status_code = status_code
        self.message = f"O titular {nome} da conta não existe"
        super().__init__(self.status_code, self.message)


class DataInvalidaException(CadastroContasException):
    def __init__(self, data: str, status_code: int = 422):
        self.status_code = status_code
        mensagem = f"A data {data} é inválida"
        super().__init__(self.status_code, mensagem)


class DataVencimentoMaiorDataPagamentoException(CadastroContasException):
    def __init__(self, data_vencimento: str, data_pagamento: str, status_code: int = 416):
        self.status_code = status_code
        mensagem = f"""A data de vencimento {data_vencimento} não pode ser maior
        que a data de pagamento {data_pagamento}!"""
        super().__init__(self.status_code, mensagem)
