import mysql.connector
from database.connect_database import conecta_banco
from typing import List, Union, cast
from interfaces.interfaces import InterfaceSubgrupoBasica, InterfaceSubgrupoCompleta


class SubgrupoDatabase:

    def __init__(self, host_name="servidorBalcao"):
        self.__conn = conecta_banco(host_name)

    def busca_dados(self, full: bool = False) -> List[Union[InterfaceSubgrupoBasica, InterfaceSubgrupoCompleta]]:
        cursor = None
        try:
            cursor = self.__conn.cursor(dictionary=True)

            query_simple = """
                SELECT cod_subgroup AS "codigo", name_subgroup AS "descricao", fixed_unit_expense AS "despesa_fixa" 
                FROM resume_subgroups
            """
            query_all = """
                SELECT 
                        cod_subgroup AS "codigo", 
                        name_subgroup AS "descricao", 
                        amount_quantity AS "quantidade",
                        amount_quantity_returned AS "quantidade_devolvida",
                        amount_invoicing AS "faturamento",
                        amount_cost AS "custo",
                        amount_discount AS "desconto",
                        amount_fixed AS "total_despesa_fixa",
                        amount_variable AS "total_despesa_variavel",
                        fixed_unit_expense AS "despesa_fixa",
                        plucro AS "porcentagem_lucro",
                        subgroup_profit AS "total_lucro",
                        discount_percentage AS "porcentagem_desconto",
                        invoicing_percentage AS "porcentagem_faturamento",
                        cost_percentage AS "porcentagem_custo",
                        fixed_expense_percentage AS "porcentagem_despesa_fixa",
                        subgroup_profit_percentage AS "porcentagem_lucro",
                        created_at AS "data_criacao",
                        updated_at AS "data_atualizacao"
                FROM resume_subgroups
            """

            cursor.execute(query_all if full else query_simple)

            resultado = cursor.fetchall()

            if full:
                return [
                    cast(InterfaceSubgrupoCompleta, {
                        "codigo": item["codigo"],
                        "descricao": item["descricao"],
                        "quantidade": float(item["quantidade"]),
                        "quantidade_devolvida": float(item["quantidade_devolvida"]),
                        "faturamento": float(item["faturamento"]),
                        "custo": float(item["custo"]),
                        "desconto": float(item["desconto"]),
                        "total_despesa_fixa": float(item["total_despesa_fixa"]),
                        "total_despesa_variavel": float(item["total_despesa_variavel"]),
                        "porcentagem_lucro": float(item["porcentagem_lucro"]),
                        "total_lucro": float(item["total_lucro"]),
                        "porcentagem_desconto": float(item["porcentagem_desconto"]),
                        "porcentagem_faturamento": float(item["porcentagem_faturamento"]),
                        "porcentagem_custo": float(item["porcentagem_custo"]),
                        "porcentagem_despesa_fixa": float(item["porcentagem_despesa_fixa"]),
                        "data_criacao": item["data_criacao"],
                        "data_atualizacao": item["data_atualizacao"]
                    })
                    for item in resultado
                ]
            else:
                return [
                    cast(InterfaceSubgrupoBasica, {
                        "codigo": item["codigo"],
                        "descricao": item["descricao"],
                        "despesa_fixa": float(item["despesa_fixa"])
                    })
                    for item in resultado
                ]
        except mysql.connector.Error as err:
            print(f"Erro ao acessar o banco de dados: {err}")
        finally:
            if cursor:
                cursor.close()
                self.__conn.close()


if __name__ == "__main__":
    busca = SubgrupoDatabase()

    for data in busca.busca_dados():
        print(data)
