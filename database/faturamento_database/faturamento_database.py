import mysql.connector
from database.connect_database import conecta_banco
from datetime import datetime, date
from ferramentas.ferramentas import validar_data
from interfaces.interfaces import InterfaceFaturamento
from typing import List, cast
import math


class FaturamentoDatabase:
    def __init__(self, host_name: str = "servidorBalcao", data_inicial: str = "", data_final: str = "",
                 comissao: float = 1):
        self.__conn = conecta_banco(host_name)
        self.__comissao = comissao / 100
        if not data_inicial and not data_final:
            self.__condicional = f'venda_item.dtvenda = "{date.today()}"'
        elif data_inicial and not data_final:
            self.__condicional = f'venda_item.dtvenda >= "{validar_data(data_inicial)}"'
        elif not data_inicial and data_final:
            self.__condicional = f'venda_item.dtvenda <= "{validar_data(data_final)}"'
        else:
            self.__condicional = (
                f'venda_item.dtvenda >= "{validar_data(data_inicial)}" '
                f'AND venda_item.dtvenda <= "{validar_data(data_final)}"'
            )

    @property
    def busca_venda_item(self):
        return self.__buscar_venda_item()

    def __buscar_venda_item(self) -> List[InterfaceFaturamento]:
        cursor = None

        try:
            cursor = self.__conn.cursor(dictionary=True)
            query = f"""
                SELECT
                    venda_item.item_cod AS `codigo`,
                    venda_item.venda AS `venda`,
                    funcionario.fun_nome as `vendedor`,
                    venda_item.qtd - venda_item.qtd_devolvida AS `quantidade`,
                    produto.prod_descricao AS `descricao`,
                    (
                        venda_item.qtd - venda_item.qtd_devolvida
                    ) * venda_item.vrcusto_composicao AS `custo`,
                    (
                        venda_item.total / venda_item.qtd
                    ) * (
                        venda_item.qtd - venda_item.qtd_devolvida
                    ) AS `faturamento`,
                    resume_subgroups.fixed_unit_expense * (
                        venda_item.qtd - venda_item.qtd_devolvida
                    ) AS `despesa_fixa`,
                    (
                        venda_item.total / venda_item.qtd
                    ) * (
                        venda_item.qtd - venda_item.qtd_devolvida
                    ) * (SELECT variable_expense_percentage FROM total_values WHERE id = "531530d9-bc36-4997-b9a6-ed664a1096e2") AS `despesa_variavel`,
                    venda_item.dtvenda AS `data_venda`
                FROM
                    venda_item
                INNER JOIN produto ON venda_item.produto = produto.prod_cod
                INNER JOIN resume_subgroups ON resume_subgroups.cod_subgroup = produto.prod_subgrupo
                INNER JOIN venda ON venda_item.venda = venda.vend_cod
                INNER JOIN funcionario ON venda.vendedor = funcionario.fun_cod
                WHERE {self.__condicional};
            """
            cursor.execute(query)
            resultado = cursor.fetchall()

            resultado = [
                cast(InterfaceFaturamento, {
                    "codigo": item["codigo"],
                    "venda": item["venda"],
                    "vendedor": item["vendedor"],
                    "quantidade": item["quantidade"],
                    "descricao": item["descricao"],
                    "faturamento": item["faturamento"],
                    "custo": item["custo"],
                    "comissao": round(item["faturamento"] * self.__comissao, 2) if
                    (item["custo"] +
                     item["despesa_variavel"] +
                     item["despesa_fixa"] +
                     item["faturamento"] * self.__comissao) < item["faturamento"] else 0.00,
                    "despesa_variavel": round(item["despesa_variavel"], 2),
                    "despesa_fixa": item["despesa_fixa"],
                    "data_venda": item["data_venda"]
                })
                for item in resultado
            ]

            return resultado

        except mysql.connector.Error as err:
            print(f"Erro ao acessar o banco de dados: {err}")
            return []

        finally:
            if cursor:
                cursor.close()
                self.__conn.close()


if __name__ == "__main__":
    busca = FaturamentoDatabase()
    for produto in busca.busca_venda_item:
        print(produto)
