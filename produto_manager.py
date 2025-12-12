"""
Módulo para gerenciamento de produtos
"""
import json
import os
from typing import List, Dict, Optional


class ProdutoManager:
    def __init__(self, data_file: str = "produtos.json"):
        """Inicializa o gerenciador de produtos"""
        self.data_file = data_file
        self.produtos: List[Dict] = []
        self.proximo_id = 1
        self._carregar_dados()

    def _carregar_dados(self):
        """Carrega os dados do arquivo JSON se existir"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, "r", encoding="utf-8") as f:
                    self.produtos = json.load(f)
                    if self.produtos:
                        # Encontra o maior ID para continuar a sequência
                        self.proximo_id = max(p["id"] for p in self.produtos) + 1
            except (json.JSONDecodeError, KeyError):
                self.produtos = []
                self.proximo_id = 1

    def _salvar_dados(self):
        """Salva os dados no arquivo JSON"""
        with open(self.data_file, "w", encoding="utf-8") as f:
            json.dump(self.produtos, f, ensure_ascii=False, indent=2)

    def adicionar_produto(self, produto: str, quantidade: int, valor: float) -> Dict:
        """
        Adiciona um novo produto ao estoque

        Args:
            produto: Nome do produto (obrigatório)
            quantidade: Quantidade em estoque (obrigatório)
            valor: Valor unitário do produto (obrigatório)

        Returns:
            Dict com o produto adicionado

        Raises:
            ValueError: Se algum campo obrigatório estiver vazio ou inválido
        """
        if not produto or not produto.strip():
            raise ValueError("Nome do produto é obrigatório")

        if quantidade < 0:
            raise ValueError("Quantidade deve ser maior ou igual a zero")

        if valor <= 0:
            raise ValueError("Valor deve ser maior que zero")

        novo_produto = {
            "id": self.proximo_id,
            "produto": produto.strip(),
            "quantidade": int(quantidade),
            "valor": float(valor),
        }

        self.produtos.append(novo_produto)
        self.proximo_id += 1
        self._salvar_dados()

        return novo_produto

    def listar_produtos(self) -> List[Dict]:
        """
        Lista todos os produtos

        Returns:
            Lista de produtos
        """
        return self.produtos.copy()

    def listar_produtos_alfabetica(self) -> List[Dict]:
        """
        Lista todos os produtos em ordem alfabética

        Returns:
            Lista de produtos ordenada por nome
        """
        return sorted(self.produtos, key=lambda p: p["produto"].lower())

    def buscar_produto_por_id(self, produto_id: int) -> Optional[Dict]:
        """
        Busca um produto por ID

        Args:
            produto_id: ID do produto

        Returns:
            Produto encontrado ou None
        """
        for produto in self.produtos:
            if produto["id"] == produto_id:
                return produto
        return None

    def buscar_produto_por_nome(self, nome: str) -> Optional[Dict]:
        """
        Busca um produto por nome (case-insensitive)

        Args:
            nome: Nome do produto

        Returns:
            Produto encontrado ou None
        """
        nome_lower = nome.lower().strip()
        for produto in self.produtos:
            if produto["produto"].lower() == nome_lower:
                return produto
        return None

    def comprar_produto(self, produto_id: int, quantidade: int, confirmar: bool = False) -> Dict:
        """
        Processa a compra de um produto

        Args:
            produto_id: ID do produto
            quantidade: Quantidade a comprar
            confirmar: Se True, efetua a compra; se False, apenas calcula o total

        Returns:
            Dict com informações da compra: {
                'produto': dict do produto,
                'quantidade': quantidade solicitada,
                'total': valor total,
                'disponivel': bool indicando se há estoque,
                'confirmado': bool indicando se a compra foi efetivada
            }

        Raises:
            ValueError: Se o produto não existir ou quantidade for inválida
        """
        if quantidade <= 0:
            raise ValueError("Quantidade deve ser maior que zero")

        produto = self.buscar_produto_por_id(produto_id)
        if not produto:
            raise ValueError(f"Produto com ID {produto_id} não encontrado")

        disponivel = produto["quantidade"] >= quantidade
        total = produto["valor"] * quantidade

        resultado = {
            "produto": produto.copy(),
            "quantidade": quantidade,
            "total": total,
            "disponivel": disponivel,
            "confirmado": False,
        }

        if confirmar:
            if not disponivel:
                raise ValueError(
                    f"Quantidade insuficiente em estoque. Disponível: {produto['quantidade']}"
                )

            # Atualiza o estoque
            produto["quantidade"] -= quantidade
            self._salvar_dados()
            resultado["confirmado"] = True
            resultado["produto"] = produto.copy()

        return resultado
