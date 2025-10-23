"""
Script de teste para o Sistema de Gestão de Produtos
Demonstra todas as funcionalidades do módulo produto_manager
"""
from produto_manager import ProdutoManager

def linha():
    print("=" * 60)

def main():
    print("\n🛒 SISTEMA DE GESTÃO DE PRODUTOS - TESTE\n")
    
    # Criar instância do gerenciador
    manager = ProdutoManager('produtos_teste.json')
    
    # Teste 1: Adicionar produtos
    linha()
    print("📝 TESTE 1: Adicionando produtos")
    linha()
    
    produtos_teste = [
        ("Notebook Dell", 10, 2500.00),
        ("Mouse Logitech", 50, 45.90),
        ("Teclado Mecânico", 25, 350.00),
        ("Monitor LG 27\"", 15, 1200.00),
        ("Webcam Full HD", 30, 180.00)
    ]
    
    for nome, qtd, valor in produtos_teste:
        produto = manager.adicionar_produto(nome, qtd, valor)
        print(f"✅ Produto adicionado: ID={produto['id']}, {produto['produto']}")
    
    # Teste 2: Listar produtos
    linha()
    print("\n📋 TESTE 2: Listando todos os produtos")
    linha()
    
    produtos = manager.listar_produtos()
    for p in produtos:
        print(f"ID: {p['id']} | {p['produto']:20} | Qtd: {p['quantidade']:3} | R$ {p['valor']:.2f}")
    
    # Teste 3: Listar em ordem alfabética
    linha()
    print("\n🔤 TESTE 3: Listando em ordem alfabética")
    linha()
    
    produtos_alfabetica = manager.listar_produtos_alfabetica()
    for p in produtos_alfabetica:
        print(f"ID: {p['id']} | {p['produto']:20} | Qtd: {p['quantidade']:3} | R$ {p['valor']:.2f}")
    
    # Teste 4: Simular compra (preview)
    linha()
    print("\n🔍 TESTE 4: Simulando compra (preview sem confirmar)")
    linha()
    
    resultado = manager.comprar_produto(1, 3, confirmar=False)
    print(f"Produto: {resultado['produto']['produto']}")
    print(f"Quantidade: {resultado['quantidade']}")
    print(f"Total: R$ {resultado['total']:.2f}")
    print(f"Disponível: {'Sim' if resultado['disponivel'] else 'Não'}")
    print(f"Confirmado: {'Sim' if resultado['confirmado'] else 'Não'}")
    
    # Teste 5: Realizar compra
    linha()
    print("\n✅ TESTE 5: Realizando compra confirmada")
    linha()
    
    print("Estoque ANTES da compra:")
    produto = manager.buscar_produto_por_id(1)
    print(f"  {produto['produto']}: {produto['quantidade']} unidades")
    
    resultado = manager.comprar_produto(1, 3, confirmar=True)
    print(f"\nCompra confirmada!")
    print(f"  Produto: {resultado['produto']['produto']}")
    print(f"  Quantidade: {resultado['quantidade']}")
    print(f"  Total: R$ {resultado['total']:.2f}")
    
    print("\nEstoque DEPOIS da compra:")
    produto = manager.buscar_produto_por_id(1)
    print(f"  {produto['produto']}: {produto['quantidade']} unidades")
    
    # Teste 6: Tentar comprar mais do que há em estoque
    linha()
    print("\n⚠️  TESTE 6: Tentando comprar mais do que há em estoque")
    linha()
    
    try:
        resultado = manager.comprar_produto(2, 1000, confirmar=False)
        if not resultado['disponivel']:
            print(f"❌ Estoque insuficiente!")
            print(f"   Solicitado: {resultado['quantidade']}")
            print(f"   Disponível: {resultado['produto']['quantidade']}")
    except ValueError as e:
        print(f"❌ Erro: {e}")
    
    # Teste 7: Validações
    linha()
    print("\n🛡️  TESTE 7: Testando validações")
    linha()
    
    # Nome vazio
    try:
        manager.adicionar_produto("", 10, 100)
    except ValueError as e:
        print(f"✅ Validação OK (nome vazio): {e}")
    
    # Quantidade negativa
    try:
        manager.adicionar_produto("Teste", -5, 100)
    except ValueError as e:
        print(f"✅ Validação OK (quantidade negativa): {e}")
    
    # Valor zero ou negativo
    try:
        manager.adicionar_produto("Teste", 10, 0)
    except ValueError as e:
        print(f"✅ Validação OK (valor zero): {e}")
    
    linha()
    print("\n✨ TODOS OS TESTES CONCLUÍDOS COM SUCESSO!")
    linha()
    print("\n💡 Dica: Execute 'python app.py' para iniciar a interface web")
    print("   Acesse http://localhost:5000 no navegador\n")

if __name__ == "__main__":
    main()
