from typing import List, Optional
from pydantic import BaseModel, Field

from cadastro_contas.modelos import Message, parse_openapi


class Conta(BaseModel):
    nome: str = Field(..., description="Nome do titular da conta")
    valor_original: float = Field(..., description="Valor da conta sem juros")
    data_vencimento: str = Field(..., description="Data de vencimento da conta no formato dd/mm/yyyy")
    data_pagamento: str = Field(..., description="Data de pagamento da conta no formato dd/mm/yyyy")


class InformacoesConta(BaseModel):
    nome: str = Field(..., description="Nome do titular da conta")
    valor_original: str = Field(..., description="Valor da conta sem juros")
    dias_atraso: str = Field(..., description="Quantidade de dias que a conta esta atrasada")
    valor_corrigido: str = Field(..., description="Valor da conta acrescidos de juros e multa")
    data_vencimento: str = Field(..., description="Data de vencimento da conta no formato dd/mm/yyyy")
    data_pagamento: str = Field(..., description="Data de pagamento da conta no formato dd/mm/yyyy")


class InserirContaResponse(BaseModel):
    resultado: List[bool] = Field(..., description="Indicação se a conta foi ou não criada")


class AtualizarContaRequest(BaseModel):
    nome: Optional[str] = Field(description="Nome do titular da conta")
    valor_original: Optional[float] = Field(description="Valor da conta sem juros")
    data_vencimento: Optional[str] = Field(description="Data de vencimento da conta no formato dd/mm/yyyy")
    data_pagamento: Optional[str] = Field(description="Data de pagamento da conta no formato dd/mm/yyyy")


class AtualizarContaResponse(BaseModel):
    resultado: List[bool] = Field(..., description="Indicação se o usuário foi ou não atualizado")


class DeletarContaResponse(BaseModel):
    resultado: List[bool] = Field(..., description="Indicação se a operação foi executada ou não")


class ListarContasTitularResponse(BaseModel):
    resultado: List[InformacoesConta] = Field(..., description="Contas associadas a um titular")


CONTA_INSERT_DEFAULT_RESPONSE = parse_openapi([
    Message(status=416, mensagem="A data de vencimento não pode ser maior que a data de pagamento",
            stacktrace="Traceback (most recent call last): ..."),
    Message(status=422, mensagem="O formatao da data é inválido",
            stacktrace="Traceback (most recent call last): ...")
])
CONTA_UPDATE_DEFAULT_RESPONSE = parse_openapi([
    Message(status=416, mensagem="A data de vencimento não pode ser maior que a data de pagamento",
            stacktrace="Traceback (most recent call last): ..."),
    Message(status=404, mensagem="A conta informada não existe",
            stacktrace="Traceback (most recent call last): ...")
])
CONTA_DELETE_DEFAULT_RESPONSE = parse_openapi([
    Message(status=404, mensagem="A conta informada não existe",
            stacktrace="Traceback (most recent call last): ...")
])
CONTA_LISTAR_TITULAR_DEFAULT_RESPONSE = parse_openapi([
    Message(status=404, mensagem="O titular da conta não existe",
            stacktrace="Traceback (most recent call last): ...")
])
