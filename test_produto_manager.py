"""
Testes unitários para o módulo produto_manager
"""
import pytest
import os
import json
from produto_manager import ProdutoManager


@pytest.fixture
def manager():
    """Fixture que cria um gerenciador de produtos para testes"""
    test_file = "test_produtos.json"
    # Remove arquivo de teste se existir
    if os.path.exists(test_file):
        os.remove(test_file)

    manager = ProdutoManager(test_file)
    yield manager

    # Limpeza após os testes
    if os.path.exists(test_file):
        os.remove(test_file)


class TestAdicionar:
    """Testes para adicionar produtos"""

    def test_adicionar_produto_valido(self, manager):
        """Teste adicionar produto com dados válidos"""
        produto = manager.adicionar_produto("Notebook", 10, 2500.00)

        assert produto["id"] == 1
        assert produto["produto"] == "Notebook"
        assert produto["quantidade"] == 10
        assert produto["valor"] == 2500.00

    def test_adicionar_multiplos_produtos(self, manager):
        """Teste adicionar múltiplos produtos"""
        p1 = manager.adicionar_produto("Mouse", 50, 45.90)
        p2 = manager.adicionar_produto("Teclado", 25, 350.00)

        assert p1["id"] == 1
        assert p2["id"] == 2
        assert len(manager.listar_produtos()) == 2

    def test_adicionar_produto_nome_vazio(self, manager):
        """Teste adicionar produto com nome vazio deve falhar"""
        with pytest.raises(ValueError, match="Nome do produto é obrigatório"):
            manager.adicionar_produto("", 10, 100)

    def test_adicionar_produto_nome_apenas_espacos(self, manager):
        """Teste adicionar produto com apenas espaços deve falhar"""
        with pytest.raises(ValueError, match="Nome do produto é obrigatório"):
            manager.adicionar_produto("   ", 10, 100)

    def test_adicionar_produto_quantidade_negativa(self, manager):
        """Teste adicionar produto com quantidade negativa deve falhar"""
        with pytest.raises(ValueError, match="Quantidade deve ser maior ou igual a zero"):
            manager.adicionar_produto("Produto", -5, 100)

    def test_adicionar_produto_valor_zero(self, manager):
        """Teste adicionar produto com valor zero deve falhar"""
        with pytest.raises(ValueError, match="Valor deve ser maior que zero"):
            manager.adicionar_produto("Produto", 10, 0)

    def test_adicionar_produto_valor_negativo(self, manager):
        """Teste adicionar produto com valor negativo deve falhar"""
        with pytest.raises(ValueError, match="Valor deve ser maior que zero"):
            manager.adicionar_produto("Produto", 10, -50)

    def test_id_auto_increment(self, manager):
        """Teste se o ID é auto incrementado corretamente"""
        p1 = manager.adicionar_produto("P1", 1, 10)
        p2 = manager.adicionar_produto("P2", 1, 10)
        p3 = manager.adicionar_produto("P3", 1, 10)

        assert p1["id"] == 1
        assert p2["id"] == 2
        assert p3["id"] == 3


class TestListar:
    """Testes para listar produtos"""

    def test_listar_produtos_vazio(self, manager):
        """Teste listar quando não há produtos"""
        produtos = manager.listar_produtos()
        assert produtos == []

    def test_listar_produtos(self, manager):
        """Teste listar produtos"""
        manager.adicionar_produto("Notebook", 10, 2500.00)
        manager.adicionar_produto("Mouse", 50, 45.90)

        produtos = manager.listar_produtos()
        assert len(produtos) == 2
        assert produtos[0]["produto"] == "Notebook"
        assert produtos[1]["produto"] == "Mouse"

    def test_listar_produtos_alfabetica(self, manager):
        """Teste listar produtos em ordem alfabética"""
        manager.adicionar_produto("Teclado", 25, 350.00)
        manager.adicionar_produto("Mouse", 50, 45.90)
        manager.adicionar_produto("Notebook", 10, 2500.00)

        produtos = manager.listar_produtos_alfabetica()
        assert len(produtos) == 3
        assert produtos[0]["produto"] == "Mouse"
        assert produtos[1]["produto"] == "Notebook"
        assert produtos[2]["produto"] == "Teclado"

    def test_listar_produtos_alfabetica_case_insensitive(self, manager):
        """Teste ordenação alfabética case insensitive"""
        manager.adicionar_produto("zebra", 1, 10)
        manager.adicionar_produto("Abacaxi", 1, 10)
        manager.adicionar_produto("BANANA", 1, 10)

        produtos = manager.listar_produtos_alfabetica()
        assert produtos[0]["produto"] == "Abacaxi"
        assert produtos[1]["produto"] == "BANANA"
        assert produtos[2]["produto"] == "zebra"


class TestBuscar:
    """Testes para buscar produtos"""

    def test_buscar_produto_por_id_existente(self, manager):
        """Teste buscar produto por ID existente"""
        manager.adicionar_produto("Mouse", 50, 45.90)
        produto = manager.buscar_produto_por_id(1)

        assert produto is not None
        assert produto["id"] == 1
        assert produto["produto"] == "Mouse"

    def test_buscar_produto_por_id_inexistente(self, manager):
        """Teste buscar produto por ID inexistente"""
        produto = manager.buscar_produto_por_id(999)
        assert produto is None

    def test_buscar_produto_por_nome_existente(self, manager):
        """Teste buscar produto por nome existente"""
        manager.adicionar_produto("Teclado", 25, 350.00)
        produto = manager.buscar_produto_por_nome("Teclado")

        assert produto is not None
        assert produto["produto"] == "Teclado"

    def test_buscar_produto_por_nome_case_insensitive(self, manager):
        """Teste buscar produto case insensitive"""
        manager.adicionar_produto("Mouse", 50, 45.90)

        produto1 = manager.buscar_produto_por_nome("mouse")
        produto2 = manager.buscar_produto_por_nome("MOUSE")

        assert produto1 is not None
        assert produto2 is not None

    def test_buscar_produto_por_nome_inexistente(self, manager):
        """Teste buscar produto inexistente"""
        produto = manager.buscar_produto_por_nome("Inexistente")
        assert produto is None


class TestComprar:
    """Testes para comprar produtos"""

    def test_comprar_produto_preview(self, manager):
        """Teste preview de compra sem confirmar"""
        manager.adicionar_produto("Notebook", 10, 2500.00)

        resultado = manager.comprar_produto(1, 3, confirmar=False)

        assert resultado["quantidade"] == 3
        assert resultado["total"] == 7500.00
        assert resultado["disponivel"] is True
        assert resultado["confirmado"] is False

        # Estoque não deve ser alterado
        produto = manager.buscar_produto_por_id(1)
        assert produto["quantidade"] == 10

    def test_comprar_produto_confirmado(self, manager):
        """Teste compra confirmada atualiza estoque"""
        manager.adicionar_produto("Mouse", 50, 45.90)

        resultado = manager.comprar_produto(1, 5, confirmar=True)

        assert resultado["confirmado"] is True
        assert resultado["total"] == 229.50

        # Estoque deve ser atualizado
        produto = manager.buscar_produto_por_id(1)
        assert produto["quantidade"] == 45

    def test_comprar_produto_estoque_insuficiente_preview(self, manager):
        """Teste preview quando não há estoque suficiente"""
        manager.adicionar_produto("Teclado", 5, 350.00)

        resultado = manager.comprar_produto(1, 10, confirmar=False)

        assert resultado["disponivel"] is False
        assert resultado["confirmado"] is False

    def test_comprar_produto_estoque_insuficiente_confirmar(self, manager):
        """Teste confirmar compra sem estoque deve falhar"""
        manager.adicionar_produto("Monitor", 5, 1200.00)

        with pytest.raises(ValueError, match="Quantidade insuficiente em estoque"):
            manager.comprar_produto(1, 10, confirmar=True)

    def test_comprar_produto_quantidade_zero(self, manager):
        """Teste comprar quantidade zero deve falhar"""
        manager.adicionar_produto("Webcam", 30, 180.00)

        with pytest.raises(ValueError, match="Quantidade deve ser maior que zero"):
            manager.comprar_produto(1, 0, confirmar=False)

    def test_comprar_produto_quantidade_negativa(self, manager):
        """Teste comprar quantidade negativa deve falhar"""
        manager.adicionar_produto("Webcam", 30, 180.00)

        with pytest.raises(ValueError, match="Quantidade deve ser maior que zero"):
            manager.comprar_produto(1, -5, confirmar=False)

    def test_comprar_produto_inexistente(self, manager):
        """Teste comprar produto inexistente deve falhar"""
        with pytest.raises(ValueError, match="Produto com ID 999 não encontrado"):
            manager.comprar_produto(999, 1, confirmar=False)

    def test_comprar_todo_estoque(self, manager):
        """Teste comprar todo o estoque disponível"""
        manager.adicionar_produto("Headset", 10, 250.00)

        resultado = manager.comprar_produto(1, 10, confirmar=True)

        assert resultado["confirmado"] is True

        # Estoque deve ficar zerado
        produto = manager.buscar_produto_por_id(1)
        assert produto["quantidade"] == 0


class TestPersistencia:
    """Testes para persistência de dados"""

    def test_salvar_dados(self, manager):
        """Teste se dados são salvos no arquivo"""
        manager.adicionar_produto("Produto1", 10, 100.00)

        assert os.path.exists(manager.data_file)

        with open(manager.data_file, "r", encoding="utf-8") as f:
            dados = json.load(f)

        assert len(dados) == 1
        assert dados[0]["produto"] == "Produto1"

    def test_carregar_dados(self):
        """Teste se dados são carregados do arquivo"""
        test_file = "test_carregar.json"

        # Cria arquivo com dados
        dados = [
            {"id": 1, "produto": "Teste1", "quantidade": 5, "valor": 50.0},
            {"id": 2, "produto": "Teste2", "quantidade": 10, "valor": 100.0},
        ]

        with open(test_file, "w", encoding="utf-8") as f:
            json.dump(dados, f)

        # Carrega manager
        manager = ProdutoManager(test_file)

        assert len(manager.produtos) == 2
        assert manager.proximo_id == 3

        # Limpeza
        os.remove(test_file)

    def test_arquivo_json_invalido(self):
        """Teste se lida com arquivo JSON inválido"""
        test_file = "test_invalido.json"

        # Cria arquivo com JSON inválido
        with open(test_file, "w", encoding="utf-8") as f:
            f.write("{ invalid json }")

        # Deve criar manager vazio sem erro
        manager = ProdutoManager(test_file)

        assert manager.produtos == []
        assert manager.proximo_id == 1

        # Limpeza
        os.remove(test_file)


class TestIntegracao:
    """Testes de integração"""

    def test_fluxo_completo(self, manager):
        """Teste fluxo completo de uso"""
        # Adiciona produtos
        manager.adicionar_produto("Notebook", 10, 2500.00)
        manager.adicionar_produto("Mouse", 50, 45.90)
        manager.adicionar_produto("Teclado", 25, 350.00)

        # Verifica listagem
        produtos = manager.listar_produtos()
        assert len(produtos) == 3

        # Verifica ordenação
        alfabetica = manager.listar_produtos_alfabetica()
        assert alfabetica[0]["produto"] == "Mouse"

        # Faz compra
        resultado = manager.comprar_produto(1, 2, confirmar=True)
        assert resultado["confirmado"] is True

        # Verifica estoque atualizado
        produto = manager.buscar_produto_por_id(1)
        assert produto["quantidade"] == 8

    def test_operacoes_multiplas(self, manager):
        """Teste múltiplas operações consecutivas"""
        # Adiciona
        manager.adicionar_produto("P1", 100, 10.00)
        manager.adicionar_produto("P2", 100, 20.00)

        # Compra 1
        manager.comprar_produto(1, 30, confirmar=True)

        # Compra 2
        manager.comprar_produto(2, 40, confirmar=True)

        # Compra 3
        manager.comprar_produto(1, 20, confirmar=True)

        # Verifica estoques
        p1 = manager.buscar_produto_por_id(1)
        p2 = manager.buscar_produto_por_id(2)

        assert p1["quantidade"] == 50
        assert p2["quantidade"] == 60
