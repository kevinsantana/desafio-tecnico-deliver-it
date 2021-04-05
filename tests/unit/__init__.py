from fastapi.testclient import TestClient

from cadastro_contas import app

client = TestClient(app)
