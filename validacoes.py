# validacoes.py
# funcoes de validacao usadas pelo app.py
# IBM4023 - AC1 - oficina mecanica

import re
from datetime import datetime


def validar_texto(texto, minimo=2):
    """valida se um texto tem pelo menos 'minimo' caracteres, sem contar espacos nas pontas."""
    return len(texto.strip()) >= minimo


def validar_placa(placa):
    """aceita o formato antigo (abc1234) e o formato mercosul (abc1d23)."""
    limpa = placa.strip().upper().replace('-', '').replace(' ', '')
    padrao_antigo = r'^[A-Z]{3}\d{4}$'
    padrao_mercosul = r'^[A-Z]{3}\d[A-Z]\d{2}$'
    return re.match(padrao_antigo, limpa) is not None or re.match(padrao_mercosul, limpa) is not None


def validar_ano(ano_str):
    """valida se o ano e um numero inteiro dentro de uma faixa ok."""
    try:
        ano = int(ano_str)
        return 1950 <= ano <= datetime.now().year + 1
    except ValueError:
        return False


def validar_valor(valor_str):
    """valida se o valor e um numero positivo (aceita virgula ou  decimal)."""
    try:
        valor = float(valor_str.replace(',', '.'))
        return valor > 0
    except ValueError:
        return False


def validar_data(data_str):
    """valida se a data esta no formato dd/mm/aaaa."""
    try:
        datetime.strptime(data_str.strip(), '%d/%m/%Y')
        return True
    except ValueError:
        return False


if __name__ == "__main__":
    print("testes rapidos de validacoes.py")
    print(validar_placa("ABC1234"))   # True
    print(validar_placa("ABC1D23"))   # True
    print(validar_placa("123ABC"))    # False
    print(validar_ano("2020"))        # True
    print(validar_ano("1800"))        # False
    print(validar_valor("150,50"))    # True
    print(validar_data("10/08/2026")) # True
