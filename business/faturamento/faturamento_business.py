from database.faturamento_database.faturamento_database import FaturamentoDatabase
from ferramentas.ferramentas import validar_data
from interfaces.interfaces import InterfaceFaturamentoItem
from typing import List, cast


class FaturamentoBusiness:
    def __init__(self, data_inicial: str = "", data_final: str = "", comissao: float = 1):
        self.__data_inicial = data_inicial
        self.__data_final = data_final
        self.__comissao = comissao
        self.__faturamento_database = FaturamentoDatabase(data_inicial=self.__data_inicial,
                                                          data_final=self.__data_final,
                                                          comissao=self.__comissao).busca_venda_item

    @property
    def dados_venda_item(self):
        return self.__dados_venda_item()

    def __dados_venda_item(self) -> List[InterfaceFaturamentoItem]:
        dados_completos = []

        for item in self.__faturamento_database:
            novo_item = item.copy()
            custo_despesa = round((item["custo"] + item["despesa_fixa"] +
                                   item["despesa_variavel"] +
                                   item["comissao"]
                                   ), 2)
            lucro_rs = round(item["faturamento"] - custo_despesa, 2)
            lucro_porcentagem = round(lucro_rs / item["faturamento"], 2) if lucro_rs != 0 else 0.00

            novo_item["custo_despesa"] = custo_despesa
            novo_item["lucro_rs"] = lucro_rs
            novo_item["lucro_porcentagem"] = lucro_porcentagem

            dados_completos.append(novo_item)

        return dados_completos


if __name__ == "__main__":
    dados = FaturamentoBusiness()

    for dado in dados.dados_venda_item:
        print(dado)
