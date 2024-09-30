from database.connect_database import conecta_banco
from interfaces.interfaces import InterfaceFormacaoPrecoVendaDatabase
from typing import List, cast
import mysql.connector


class CriaPrecoDatabase:
    def __init__(self, host_name: str = "servidorBalcao"):
        self.__conn = conecta_banco(host_name)

    @property
    def buscar_todas_nf_abertas(self):
        return self.__buscar_todas_nf_abertas()

    def __buscar_todas_nf_abertas(self) -> List[InterfaceFormacaoPrecoVendaDatabase]:
        cursor = None

        try:

            cursor = self.__conn.cursor(dictionary=True)

            query = """
                SELECT
                    f.nf AS nota_fiscal,
                    f.`data` AS data,
                    f.total AS total_nota,
                    fornecedor.forn_nome AS nome_fornecedor,
                    i.qtdentrada AS quantidade,
                    p.prod_descricao AS descricao,
                    i.fracao AS fracao,
                    i.custo AS custo,
                    r.fixed_unit_expense AS despesa_fixa,
                    r.discount_percentage AS desconto_subgrupo,
                    subgrupo_produtos.plucro / 100 AS lucro_subgrupo
                FROM formacao_preco AS f
                INNER JOIN formacao_itens AS i ON i.formacao = f.codigo
                INNER JOIN produto AS p ON i.produto = p.prod_cod
                INNER JOIN nfc AS n ON n.nfc_codigo = f.nf_codigo
                INNER JOIN resume_subgroups AS r ON r.cod_subgroup = p.prod_subgrupo
                INNER JOIN fornecedor ON fornecedor.forn_cod = f.fornecedor
                INNER JOIN subgrupo_produtos ON subgrupo_produtos.subprod_cod = r.cod_subgroup
                WHERE n.`status` = 'F' and f.situacao = "0"
            """
            cursor.execute(query)
            resultado = cursor.fetchall()

            return [
                cast(
                    InterfaceFormacaoPrecoVendaDatabase, {
                        "nota_fiscal": item["nota_fiscal"],
                        "data": item["data"],
                        "total_nota": float(item["total_nota"]),
                        "nome_fornecedor": item["nome_fornecedor"],
                        "quantidade": float(item["quantidade"]),
                        "descricao": item["descricao"],
                        "fracao": float(item["fracao"]),
                        "custo": float(item["custo"]),
                        "despesa_fixa": float(item["despesa_fixa"]),
                        "desconto_subgrupo": float(item["desconto_subgrupo"]),
                        "lucro_subgrupo": float(item["lucro_subgrupo"])
                    }
                )
                for item in resultado
            ]

        except mysql.connector.Error as err:
            print(f"Erro ao acessar o banco de dados: {err}")
            return []

        finally:
            if cursor:
                cursor.close()
                self.__conn.close()


if __name__ == "__main__":
    busca = CriaPrecoDatabase()

    for produto in busca.buscar_todas_nf_abertas:
        print(produto)
