# dados_iniciais.py
# popula o banco com dados de exemplo
# IBM4023 - AC1 - oficina mecanica
# rodar com: python dados_iniciais.py

from banco import conectar_banco


def popular():
    conn = conectar_banco()

    # limpa o banco antes, pra poder rodar este script varias vezes sem duplicar
    conn.execute("DELETE FROM servicos")
    conn.execute("DELETE FROM veiculos")
    conn.execute("DELETE FROM sqlite_sequence WHERE name IN ('veiculos', 'servicos')")
    conn.commit()

    veiculos = [
        ("ABC1234", "Fiat", "Uno", 2015, "Maria Silva"),
        ("XYZ9A87", "Volkswagen", "Gol", 2018, "Joao Pereira"),
        ("DEF5678", "Chevrolet", "Onix", 2021, "Ana Souza"),
        ("GHI3D45", "Honda", "Civic", 2019, "Carlos Lima"),
    ]

    ids = []
    for placa, marca, modelo, ano, dono in veiculos:
        cursor = conn.execute(
            'INSERT INTO veiculos (placa, marca, modelo, ano, nome_proprietario)'
            ' VALUES (?, ?, ?, ?, ?)',
            (placa, marca, modelo, ano, dono))
        ids.append(cursor.lastrowid)
    conn.commit()

    # servicos ligados aos 3 primeiros veiculos.
    # o 4o veiculo (honda civic) fica de proposito sem nenhum servico,
    # pra testar se a pagina de detalhe aguenta a lista vazia.
    servicos = [
        (ids[0], "troca de oleo e filtro", "10/08/2026", 180.00, "sim"),
        (ids[0], "alinhamento e balanceamento", "02/09/2026", 220.00, "nao"),
        (ids[1], "revisao dos freios", "15/08/2026", 350.00, "sim"),
        (ids[2], "troca da bateria", "20/08/2026", 420.00, "nao"),
    ]

    for veiculo_id, descricao, data_entrada, valor, concluido in servicos:
        conn.execute(
            'INSERT INTO servicos (veiculo_id, descricao, data_entrada, valor, concluido)'
            ' VALUES (?, ?, ?, ?, ?)',
            (veiculo_id, descricao, data_entrada, valor, concluido))
    conn.commit()
    conn.close()

    print(f"{len(veiculos)} veiculos inseridos.")
    print(f"{len(servicos)} servicos inseridos.")
    print("o honda civic ficou sem nenhum servico, de proposito.")


if __name__ == "__main__":
    popular()
