# app.py
# rotas da aplicacao - sem nenhum html aqui dentro
# IBM4023 - AC1 - oficina mecanica

from flask import Flask, request, render_template, redirect, url_for
from banco import conectar_banco
from validacoes import validar_texto, validar_placa, validar_ano, validar_valor, validar_data

app = Flask(__name__)


# --------------------------------------------------------------- LEITURA (GET)

@app.route("/")
def listar():
    """pagina inicial: todos os veiculos cadastrados."""
    conn = conectar_banco()
    veiculos = conn.execute(
        'SELECT * FROM veiculos ORDER BY marca, modelo').fetchall()
    conn.close()

    return render_template("lista.html", veiculos=veiculos,
                           msg=request.args.get("msg", ""))


@app.route("/veiculo/<int:id_veiculo>")
def detalhe(id_veiculo):
    """pagina de um veiculo especifico, com os servicos relacionados."""
    conn = conectar_banco()
    veiculo = conn.execute('SELECT * FROM veiculos WHERE id = ?',
                           (id_veiculo,)).fetchone()

    if veiculo is None:
        conn.close()
        return render_template("erro.html",
                               mensagem=f"nao existe veiculo com id {id_veiculo}."), 404

    servicos = conn.execute(
        'SELECT * FROM servicos WHERE veiculo_id = ? ORDER BY data_entrada DESC',
        (id_veiculo,)).fetchall()
    conn.close()

    return render_template("detalhe.html", veiculo=veiculo, servicos=servicos)


@app.route("/buscar")
def buscar():
    """busca por placa, marca, modelo ou proprietario. o termo vem na url."""
    termo = request.args.get("termo", "").strip().lower()

    encontrados = []
    if termo:
        conn = conectar_banco()
        curinga = f"%{termo}%"
        encontrados = conn.execute(
            '''SELECT * FROM veiculos
               WHERE LOWER(placa) LIKE ? OR LOWER(marca) LIKE ?
                  OR LOWER(modelo) LIKE ? OR LOWER(nome_proprietario) LIKE ?
               ORDER BY marca''',
            (curinga, curinga, curinga, curinga)
        ).fetchall()
        conn.close()

    return render_template("busca.html", termo=termo, veiculos=encontrados)


# --------------------------------------------------------------- VALIDACAO

def validar_formulario(dados, conn, id_atual=None):
    """valida os dados vindos do formulario de veiculo.

    devolve um dicionario de erros: {campo: mensagem}.
    dicionario vazio significa que esta tudo certo.
    """
    erros = {}

    if not validar_texto(dados["marca"]):
        erros["marca"] = "a marca deve ter pelo menos 2 caracteres."

    if not validar_texto(dados["modelo"]):
        erros["modelo"] = "o modelo deve ter pelo menos 2 caracteres."

    if not validar_ano(dados["ano"]):
        erros["ano"] = "o ano deve ser um numero entre 1950 e 2027."

    if not validar_texto(dados["nome_proprietario"]):
        erros["nome_proprietario"] = "o nome do proprietario deve ter pelo menos 2 caracteres."

    if not validar_placa(dados["placa"]):
        erros["placa"] = "informe uma placa valida (ex: abc1234 ou abc1d23)."
    else:
        # regra que depende do banco: a placa nao pode se repetir.
        # ao editar, o proprio registro nao conta como duplicata.
        placa_normalizada = dados["placa"].upper().replace("-", "").replace(" ", "")
        if id_atual is None:
            existente = conn.execute(
                'SELECT id FROM veiculos WHERE UPPER(placa) = ?',
                (placa_normalizada,)).fetchone()
        else:
            existente = conn.execute(
                'SELECT id FROM veiculos WHERE UPPER(placa) = ? AND id <> ?',
                (placa_normalizada, id_atual)).fetchone()
        if existente:
            erros["placa"] = "ja existe um veiculo cadastrado com essa placa."

    return erros


def ler_formulario():
    """le os campos enviados e devolve um dicionario ja limpo."""
    return {
        "placa": request.form.get("placa", "").strip().upper().replace("-", "").replace(" ", ""),
        "marca": request.form.get("marca", "").strip(),
        "modelo": request.form.get("modelo", "").strip(),
        "ano": request.form.get("ano", "").strip(),
        "nome_proprietario": request.form.get("nome_proprietario", "").strip(),
    }


# --------------------------------------------------------------- CADASTRAR

@app.route("/novo", methods=["GET", "POST"])
def novo():
    """get exibe o formulario; post grava o veiculo."""
    if request.method == "GET":
        return render_template("form.html", titulo="cadastrar veiculo",
                               dados={}, erros={}, acao=url_for("novo"))

    dados = ler_formulario()

    conn = conectar_banco()
    erros = validar_formulario(dados, conn)

    if erros:
        conn.close()
        # devolve o formulario com o que foi digitado e as mensagens de erro
        return render_template("form.html", titulo="cadastrar veiculo",
                               dados=dados, erros=erros,
                               acao=url_for("novo")), 400

    conn.execute(
        'INSERT INTO veiculos (placa, marca, modelo, ano, nome_proprietario)'
        ' VALUES (?, ?, ?, ?, ?)',
        (dados["placa"], dados["marca"].title(), dados["modelo"].title(),
         int(dados["ano"]), dados["nome_proprietario"].title()))
    conn.commit()
    conn.close()

    # post-redirect-get: nunca devolver a pagina direto depois de gravar
    return redirect(url_for("listar", msg="veiculo cadastrado com sucesso."))


# --------------------------------------------------------------- EDITAR

@app.route("/veiculo/<int:id_veiculo>/editar", methods=["GET", "POST"])
def editar(id_veiculo):
    """get exibe o formulario preenchido; post grava a alteracao."""
    conn = conectar_banco()
    veiculo = conn.execute('SELECT * FROM veiculos WHERE id = ?',
                           (id_veiculo,)).fetchone()

    if veiculo is None:
        conn.close()
        return render_template("erro.html",
                               mensagem=f"nao existe veiculo com id {id_veiculo}."), 404

    if request.method == "GET":
        conn.close()
        # dict(veiculo) converte a linha do banco em dicionario
        return render_template("form.html", titulo=f"editar {veiculo['placa']}",
                               dados=dict(veiculo), erros={},
                               acao=url_for("editar", id_veiculo=id_veiculo))

    dados = ler_formulario()
    erros = validar_formulario(dados, conn, id_atual=id_veiculo)

    if erros:
        conn.close()
        return render_template("form.html", titulo=f"editar {veiculo['placa']}",
                               dados=dados, erros=erros,
                               acao=url_for("editar", id_veiculo=id_veiculo)), 400

    conn.execute(
        'UPDATE veiculos SET placa = ?, marca = ?, modelo = ?, ano = ?,'
        ' nome_proprietario = ? WHERE id = ?',
        (dados["placa"], dados["marca"].title(), dados["modelo"].title(),
         int(dados["ano"]), dados["nome_proprietario"].title(), id_veiculo))
    conn.commit()
    conn.close()

    return redirect(url_for("listar", msg="dados atualizados com sucesso."))


# --------------------------------------------------------------- EXCLUIR

@app.route("/veiculo/<int:id_veiculo>/excluir", methods=["POST"])
def excluir(id_veiculo):
    """exclui o veiculo. aceita somente post - um link nao pode apagar dados."""
    conn = conectar_banco()
    veiculo = conn.execute('SELECT * FROM veiculos WHERE id = ?',
                           (id_veiculo,)).fetchone()

    if veiculo is None:
        conn.close()
        return render_template("erro.html",
                               mensagem=f"nao existe veiculo com id {id_veiculo}."), 404

    # apaga primeiro os servicos ligados a esse veiculo (senao ficam orfaos no banco)
    conn.execute('DELETE FROM servicos WHERE veiculo_id = ?', (id_veiculo,))
    conn.execute('DELETE FROM veiculos WHERE id = ?', (id_veiculo,))
    conn.commit()
    conn.close()

    return redirect(url_for("listar",
                            msg=f"veiculo de placa {veiculo['placa']} excluido."))


@app.errorhandler(404)
def pagina_nao_encontrada(erro):
    return render_template("erro.html",
                           mensagem="confira o endereco digitado."), 404


if __name__ == "__main__":
    app.run(debug=True)
