from fastapi import APIRouter, Body, Query

from cadastro_contas.modelos.juros import Juros
from cadastro_contas.modulos import juros as jrs
from cadastro_contas.modelos.juros import ListarJurosResponse, JUROS_LISTAR_DEFAULT_RESPONSE
from cadastro_contas.modelos.juros import InserirJurosResponse, JUROS_INSERT_DEFAULT_RESPONSE
from cadastro_contas.modelos.juros import DeletarJurosResponse, JUROS_DELETE_DEFAULT_RESPONSE
from cadastro_contas.modelos.juros import AtualizarJurosRequest, AtualizarJurosResponse, JUROS_UPDATE_DEFAULT_RESPONSE


router = APIRouter()


@router.post("/", status_code=200, summary="Insere uma nova regra de juros", response_model=InserirJurosResponse,
             responses=JUROS_INSERT_DEFAULT_RESPONSE)
def inserir(
    dados_juros: Juros = Body(
        ...,
        example={
            "dias_em_atraso": 3,
            "porcentagem_multa": 5,
            "juros_por_dia": 0.2
        }
    )
):
    """
    Endpoint para efetuar a gravação de uma regra de juros no banco de dados.
    """
    return {"resultado": [jrs.inserir(**dados_juros.dict())]}


@router.put("/{id_juros}", status_code=200, summary="Atualizar uma regra de juros",
            response_model=AtualizarJurosResponse, responses=JUROS_UPDATE_DEFAULT_RESPONSE)
def atualizar(id_juros: int = Query(..., description="Identificador da regra de juros"),
              dados_atualizacao: AtualizarJurosRequest = Body(..., description="Dados relativos a atualização")):
    """
    Atualiza uma regra de juros.
    """
    return {"resultado": [jrs.atualizar(id_juros=id_juros, **dados_atualizacao.dict())]}


@router.delete("/{id_juros}", status_code=200, summary="Deleta uma regra de juros",
               response_model=DeletarJurosResponse, responses=JUROS_DELETE_DEFAULT_RESPONSE)
def deletar(id_juros: int = Query(..., description="Identificador da regra de juros")):
    return {"resultado": [jrs.deletar(id_juros=id_juros)]}


@router.get("/", status_code=200, summary="Listar as regras de juros",
            response_model=ListarJurosResponse, responses=JUROS_LISTAR_DEFAULT_RESPONSE)
def listar_contas_titular():
    """
    Lista regras de juros disponíveis no banco de dados.
    """
    return {"resultado": jrs.listar()}
