from fastapi import APIRouter, Body

from cadastro_contas.modulos import conta as cnt
from cadastro_contas.modelos.conta import Conta
from cadastro_contas.modelos.conta import InserirContaResponse, CONTA_INSERT_DEFAULT_RESPONSE


router = APIRouter()


@router.post("/", status_code=200, summary="Insere uma conta", response_model=InserirContaResponse,
             responses=CONTA_INSERT_DEFAULT_RESPONSE)
def inserir(
    dados_conta: Conta = Body(
        ...,
        example={
            "nome": "Jose da Silva",
            "valor_original": "1407.31",
            "data_vencimento": "01/04/2021",
            "data_pagamento": "03/04/2021"
        }
    )
):
    """
    Endpoint para efetuar a gravação de uma conta no banco de dados.
    """
    return {"resultado": [cnt.inserir(**dados_conta.dict())]}
