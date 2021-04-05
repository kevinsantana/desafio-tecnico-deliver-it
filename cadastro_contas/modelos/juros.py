from typing import List, Optional
from pydantic import BaseModel, Field

from cadastro_contas.modelos import Message, parse_openapi


class Juros(BaseModel):
    dias_em_atraso: int = Field(..., description="Dias de atraso para o qual a regra se aplica")
    porcentagem_multa: int = Field(..., description="Porcentagem da multa aplicada a regra")
    juros_por_dia: float = Field(..., description="Valor de juros aplicados por dia de atraso")


class InserirJurosResponse(BaseModel):
    resultado: List[bool] = Field(..., description="Indicação se a regra de juros foi ou não criada")


class AtualizarJurosRequest(BaseModel):
    dias_em_atraso: Optional[int] = Field(description="Dias de atraso para o qual a regra se aplica")
    porcentagem_multa: Optional[int] = Field(description="Porcentagem da multa aplicada a regra")
    juros_por_dia: Optional[float] = Field(description="Valor de juros aplicados por dia de atraso")


class AtualizarJurosResponse(BaseModel):
    resultado: List[bool] = Field(..., description="Indicação se o usuário foi ou não atualizado")


class DeletarJurosResponse(BaseModel):
    resultado: List[bool] = Field(..., description="Indicação se a operação foi executada ou não")


class ListarJurosResponse(BaseModel):
    resultado: List[Juros] = Field(..., description="Lista de dicionários em que cada item é uma regra")


JUROS_INSERT_DEFAULT_RESPONSE = parse_openapi()

JUROS_UPDATE_DEFAULT_RESPONSE = parse_openapi([
    Message(status=404, mensagem="A regra de juros não existe",
            stacktrace="Traceback (most recent call last): ...")
])

JUROS_DELETE_DEFAULT_RESPONSE = parse_openapi([
    Message(status=404, mensagem="A regra de juros não existe",
            stacktrace="Traceback (most recent call last): ...")
])

JUROS_LISTAR_TITULAR_DEFAULT_RESPONSE = parse_openapi([
    Message(status=404, mensagem="O titular da conta não existe",
            stacktrace="Traceback (most recent call last): ...")
])

JUROS_LISTAR_DEFAULT_RESPONSE = parse_openapi()
