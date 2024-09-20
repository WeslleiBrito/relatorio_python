from datetime import datetime, date
import re


def validar_data(data_str: str) -> date:
    formato = "%Y-%m-%d"

    try:
        # Tenta converter a string para uma data no formato especificado
        data = datetime.strptime(data_str, formato)
        return data.date()
    except ValueError:
        raise ValueError(f"Data inválida: {data_str}")


def extrair_primeiros_nomes(nome):
    # Lista de conjunções comuns que devem ser incluídas
    conjuncoes = ['DE', 'DA', 'DO', 'DAS', 'DOS']

    # Divide o nome em partes
    partes = nome.split()

    # Inicializa a lista dos primeiros nomes
    resultado = [partes[0]]

    # Itera pelas partes do nome, incluindo o segundo nome e, se houver conjunção, o nome seguinte
    for i in range(1, len(partes)):
        if partes[i].upper() in conjuncoes:
            resultado.append(partes[i])  # Adiciona a conjunção
            if i + 1 < len(partes):
                resultado.append(partes[i + 1])  # Adiciona o nome seguinte à conjunção
            break
        else:
            resultado.append(partes[i])  # Adiciona o segundo nome normal
            break

    return ' '.join(resultado)


if __name__ == "__main__":
    print(validar_data("1970-01-01"))
