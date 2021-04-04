from fastapi import APIRouter

from cadastro_contas.rotas.v1 import conta, healthcheck


v1 = APIRouter()
v1.include_router(healthcheck.router, prefix="/health", tags=["healthcheck"])
v1.include_router(conta.router, prefix="/conta", tags=["contas"])
