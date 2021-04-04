from math import ceil

from loguru import logger


def montar_paginacao(dados: list, quantidade: int, pagina: int, total: int, url: str) -> dict:
    total, identificador = ceil(total/quantidade), ""
    resposta = {"resultado": dados, "paginacao": {
        "proxima": "", "anterior": "", "primeira": "", "ultima": "", "total": total
    }}
    endpoint, params = url.split("?")
    logger.debug(params)
    if params.startswith('quantidade'):
        _, _, *outros = params.split("&")
    else:
        identificador, _, _, *outros = params.split("&")
    if len(dados) == quantidade and pagina < total:
        proxima = '&'.join([identificador, f"quantidade={quantidade}", f"pagina={pagina+1}", *outros])
        resposta["paginacao"]["proxima"] = f"{endpoint}?{proxima}"
    if pagina > 1 and pagina <= total:
        anterior = '&'.join([identificador, f"quantidade={quantidade}", f"pagina={pagina-1}", *outros])
        resposta["paginacao"]["anterior"] = f"{endpoint}?{anterior}"
    ultima = '&'.join([identificador, f"quantidade={quantidade}", f"pagina={total}", *outros])
    primeira = '&'.join([identificador, f"quantidade={quantidade}", "pagina=1", *outros])
    if pagina > 1:
        resposta["paginacao"]["primeira"] = f"{endpoint}?{primeira}"
    if pagina < total:
        resposta["paginacao"]["ultima"] = f"{endpoint}?{ultima}"
    return resposta
