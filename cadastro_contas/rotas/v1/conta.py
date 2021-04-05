from fastapi import APIRouter, Body, Query

from cadastro_contas.modulos import conta as cnt
from cadastro_contas.modelos.conta import Conta
from cadastro_contas.modelos.conta import AtualizarContaRequest, AtualizarContaResponse, CONTA_UPDATE_DEFAULT_RESPONSE
from cadastro_contas.modelos.conta import InserirContaResponse, CONTA_INSERT_DEFAULT_RESPONSE
from cadastro_contas.modelos.conta import DeletarContaResponse, CONTA_DELETE_DEFAULT_RESPONSE
from cadastro_contas.modelos.conta import ListarContasTitularResponse, CONTA_LISTAR_TITULAR_DEFAULT_RESPONSE


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


@router.put("/{id_conta}", status_code=200, summary="Atualizar uma conta", response_model=AtualizarContaResponse,
            responses=CONTA_UPDATE_DEFAULT_RESPONSE)
def atualizar(id_conta: int = Query(..., description="Identificador da conta"),
              dados_atualizacao: AtualizarContaRequest = Body(..., description="Dados relativos a atualização")):
    """
    Atualiza uma conta.
    """
    return {"resultado": [cnt.atualizar(id_conta=id_conta, **dados_atualizacao.dict())]}


@router.delete("/{id_conta}", status_code=200, summary="Deleta uma conta",
               response_model=DeletarContaResponse, responses=CONTA_DELETE_DEFAULT_RESPONSE)
def deletar(id_conta: int = Query(..., description="Identificador da conta")):
    return {"resultado": [cnt.deletar(id_conta=id_conta)]}


@router.get("/{nome_titular}", status_code=200, summary="Listar as contas de um titular",
            response_model=ListarContasTitularResponse, responses=CONTA_LISTAR_TITULAR_DEFAULT_RESPONSE)
def listar_contas_titular(nome: str = Query(..., description="Nome do titular das contas")):
    """
    Lista contas de um titular.
    """
    return {"resultado": cnt.listar_contas_titular(nome=nome)}
