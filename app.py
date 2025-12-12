"""
Aplicação Flask para gerenciamento de produtos
"""
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from produto_manager import ProdutoManager
import os

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-key-change-in-production")

# Inicializa o gerenciador de produtos
manager = ProdutoManager()


@app.route("/")
def index():
    """Página inicial com lista de produtos"""
    produtos = manager.listar_produtos()
    return render_template("index.html", produtos=produtos)


@app.route("/alfabetica")
def listar_alfabetica():
    """Lista produtos em ordem alfabética"""
    produtos = manager.listar_produtos_alfabetica()
    return render_template("index.html", produtos=produtos, ordenado=True)


@app.route("/adicionar", methods=["GET", "POST"])
def adicionar_produto():
    """Adiciona um novo produto"""
    if request.method == "POST":
        try:
            produto = request.form.get("produto", "").strip()
            quantidade = int(request.form.get("quantidade", 0))
            valor = float(request.form.get("valor", 0))

            novo_produto = manager.adicionar_produto(produto, quantidade, valor)
            flash(f'Produto "{novo_produto["produto"]}" adicionado com sucesso!', "success")
            return redirect(url_for("index"))

        except ValueError as e:
            flash(f"Erro: {str(e)}", "error")
        except Exception as e:
            flash(f"Erro inesperado: {str(e)}", "error")

    return render_template("adicionar.html")


@app.route("/comprar/<int:produto_id>", methods=["GET", "POST"])
def comprar_produto(produto_id):
    """Processa a compra de um produto"""
    produto = manager.buscar_produto_por_id(produto_id)

    if not produto:
        flash("Produto não encontrado!", "error")
        return redirect(url_for("index"))

    if request.method == "POST":
        try:
            quantidade = int(request.form.get("quantidade", 0))
            confirmar = request.form.get("confirmar") == "true"

            resultado = manager.comprar_produto(produto_id, quantidade, confirmar)

            if confirmar:
                flash(
                    f'Compra realizada com sucesso! Total: R$ {resultado["total"]:.2f}', "success"
                )
                return redirect(url_for("index"))
            else:
                # Exibe prévia da compra
                return render_template(
                    "comprar.html",
                    produto=produto,
                    quantidade=quantidade,
                    total=resultado["total"],
                    disponivel=resultado["disponivel"],
                    preview=True,
                )

        except ValueError as e:
            flash(f"Erro: {str(e)}", "error")
        except Exception as e:
            flash(f"Erro inesperado: {str(e)}", "error")

    return render_template("comprar.html", produto=produto)


# API Endpoints (opcional, para facilitar integração)
@app.route("/api/produtos", methods=["GET"])
def api_listar_produtos():
    """API: Lista todos os produtos"""
    produtos = manager.listar_produtos()
    return jsonify(produtos)


@app.route("/api/produtos/alfabetica", methods=["GET"])
def api_listar_alfabetica():
    """API: Lista produtos em ordem alfabética"""
    produtos = manager.listar_produtos_alfabetica()
    return jsonify(produtos)


@app.route("/api/produtos", methods=["POST"])
def api_adicionar_produto():
    """API: Adiciona um novo produto"""
    try:
        data = request.get_json()
        produto = manager.adicionar_produto(data["produto"], data["quantidade"], data["valor"])
        return jsonify(produto), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/comprar", methods=["POST"])
def api_comprar_produto():
    """API: Processa compra de produto"""
    try:
        data = request.get_json()
        resultado = manager.comprar_produto(
            data["produto_id"], data["quantidade"], data.get("confirmar", False)
        )
        return jsonify(resultado), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
