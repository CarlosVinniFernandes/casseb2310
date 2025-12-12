"""
Testes unitários para a aplicação Flask
"""
import pytest
import json
from app import app as flask_app
from produto_manager import ProdutoManager
import os


@pytest.fixture
def app():
    """Fixture da aplicação Flask"""
    flask_app.config["TESTING"] = True
    flask_app.config["SECRET_KEY"] = "test-secret-key"

    # Importa o manager da app e reseta
    from app import manager

    manager.produtos = []
    manager.proximo_id = 1

    yield flask_app

    # Limpeza
    manager.produtos = []
    manager.proximo_id = 1
    if os.path.exists("produtos.json"):
        os.remove("produtos.json")


@pytest.fixture
def client(app):
    """Fixture do cliente de teste"""
    return app.test_client()


class TestRotasPrincipais:
    """Testes das rotas principais"""

    def test_index_vazio(self, client):
        """Teste página inicial sem produtos"""
        response = client.get("/")
        assert response.status_code == 200
        assert b"Lista de Produtos" in response.data or b"Nenhum produto" in response.data

    def test_adicionar_get(self, client):
        """Teste GET da página adicionar"""
        response = client.get("/adicionar")
        assert response.status_code == 200
        assert b"Adicionar" in response.data

    def test_alfabetica(self, client):
        """Teste rota alfabética"""
        response = client.get("/alfabetica")
        assert response.status_code == 200


class TestAdicionarProduto:
    """Testes para adicionar produtos via web"""

    def test_adicionar_produto_valido(self, client):
        """Teste adicionar produto válido via POST"""
        response = client.post(
            "/adicionar",
            data={"produto": "Notebook", "quantidade": "10", "valor": "2500.00"},
            follow_redirects=True,
        )

        assert response.status_code == 200
        assert b"sucesso" in response.data or b"adicionado" in response.data

    def test_adicionar_produto_invalido(self, client):
        """Teste adicionar produto inválido"""
        response = client.post(
            "/adicionar",
            data={"produto": "", "quantidade": "10", "valor": "100"},
            follow_redirects=True,
        )

        assert response.status_code == 200


class TestAPI:
    """Testes da API REST"""

    def test_api_listar_produtos_vazio(self, client):
        """Teste API listar produtos vazio"""
        response = client.get("/api/produtos")
        assert response.status_code == 200

        data = json.loads(response.data)
        assert isinstance(data, list)

    def test_api_adicionar_produto(self, client):
        """Teste API adicionar produto"""
        response = client.post(
            "/api/produtos",
            data=json.dumps({"produto": "Mouse", "quantidade": 50, "valor": 45.90}),
            content_type="application/json",
        )

        assert response.status_code == 201
        data = json.loads(response.data)
        assert data["produto"] == "Mouse"
        assert data["id"] == 1

    def test_api_adicionar_produto_invalido(self, client):
        """Teste API adicionar produto inválido"""
        response = client.post(
            "/api/produtos",
            data=json.dumps({"produto": "", "quantidade": 10, "valor": 100}),
            content_type="application/json",
        )

        assert response.status_code == 400

    def test_api_listar_alfabetica(self, client):
        """Teste API listar em ordem alfabética"""
        # Adiciona produtos
        client.post(
            "/api/produtos",
            data=json.dumps({"produto": "Zebra", "quantidade": 1, "valor": 10}),
            content_type="application/json",
        )
        client.post(
            "/api/produtos",
            data=json.dumps({"produto": "Abacaxi", "quantidade": 1, "valor": 10}),
            content_type="application/json",
        )

        response = client.get("/api/produtos/alfabetica")
        assert response.status_code == 200

        data = json.loads(response.data)
        assert data[0]["produto"] == "Abacaxi"
        assert data[1]["produto"] == "Zebra"
