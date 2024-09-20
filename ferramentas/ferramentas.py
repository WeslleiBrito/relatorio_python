from datetime import datetime, date


def validar_data(data_str: str) -> date:
    formato = "%Y-%m-%d"

    try:
        # Tenta converter a string para uma data no formato especificado
        data = datetime.strptime(data_str, formato)
        return data.date()
    except ValueError:
        raise ValueError(f"Data inválida: {data_str}")


if __name__ == "__main__":
    print(validar_data("1970-01-01"))
