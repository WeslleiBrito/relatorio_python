from database.faturamento_database.faturamento_database import FaturamentoDatabase
from ferramentas.ferramentas import validar_data
from interfaces.interfaces import (
    InterfaceFaturamentoItem, 
    InterfaceVendaItemCompleto, 
    InterfaceResumo, 
    InterfacePeriodoApuracao
)
from typing import List, cast
from datetime import date, datetime


class FaturamentoBusiness:
    def __init__(self, data_inicial: str = "", data_final: str = "", comissao: float = 1):
        self.__data_inicial = data_inicial
        self.__data_final = data_final
        self.__comissao = comissao
        self.__periodo_de_apuracao: InterfacePeriodoApuracao = {
            "data_inicial": "",
            "data_final": ""
        }

        if not data_inicial and not data_final:
            data_atual = date.today()
            self.__condicional = f'venda_item.dtvenda = "{data_atual}"'
            self.__periodo_de_apuracao["data_inicial"] = data_atual.strftime('%d/%m/%Y')
            self.__periodo_de_apuracao["data_final"] = data_atual.strftime('%d/%m/%Y')

        elif data_inicial and not data_final:
            data_valida = validar_data(data_inicial)
            self.__condicional = f'venda_item.dtvenda >= "{data_valida}"'
            self.__periodo_de_apuracao["data_inicial"] = data_valida.strftime('%d/%m/%Y')
            self.__periodo_de_apuracao["data_final"] = date.today().strftime('%d/%m/%Y')
        elif not data_inicial and data_final:
            self.__condicional = f'venda_item.dtvenda <= "{validar_data(data_final)}"'
        else:
            data_i = validar_data(data_inicial)
            data_f = validar_data(data_final)
            self.__condicional = (
                f'venda_item.dtvenda >= "{data_i}" '
                f'AND venda_item.dtvenda <= "{data_f}"'
            )
            self.__periodo_de_apuracao["data_inicial"] = data_i.strftime('%d/%m/%Y')
            self.__periodo_de_apuracao["data_final"] = data_f.strftime('%d/%m/%Y')

        self.__faturamento_database = FaturamentoDatabase(condicao_busca=self.__condicional,
                                                          comissao=self.__comissao).busca_venda_item

    @property
    def dados_venda_item(self):
        return self.__dados_venda_item()

    def __dados_venda_item(self) -> InterfaceVendaItemCompleto:
        dados_completos = []

        for item in self.__faturamento_database:
            novo_item = item.copy()
            custo_despesa = round((item["custo"] + item["despesa_fixa"] +
                                   item["despesa_variavel"] +
                                   item["comissao"]
                                   ), 2)
            lucro_rs = round(item["faturamento"] - custo_despesa, 2)
            lucro_porcentagem = round(lucro_rs / item["faturamento"], 3) if lucro_rs != 0 else 0.00

            novo_item["custo_despesa"] = custo_despesa
            novo_item["lucro_rs"] = lucro_rs
            novo_item["lucro_porcentagem"] = lucro_porcentagem

            dados_completos.append(novo_item)

        if not self.__data_inicial and self.__data_final:
            data_i = dados_completos[0]["data_venda"].strftime('%d/%m/%Y')
            data_f = validar_data(self.__data_final).strftime('%d/%m/%Y')

            self.__periodo_de_apuracao["data_inicial"] = data_i
            self.__periodo_de_apuracao["data_final"] = data_f

        return {
            "dados_unitarios": dados_completos,
            "resumo": self.__dados_venda_item_completo(dados_completos),
            "periodo_apuracao": self.__periodo_de_apuracao
        }

    @staticmethod
    def __dados_venda_item_completo(dados_venda_item: List[InterfaceFaturamentoItem]) -> InterfaceResumo:
        faturamento = 0.00
        custo = 0.00
        despesa_variavel = 0.00
        despesa_fixa = 0.00
        comissao = 0.00
        negativo = 0.00
        lucro_rs = 0.00
        lucro_percentual = 0.00

        for item in dados_venda_item:
            faturamento += item["faturamento"]
            custo += item["custo"]
            despesa_variavel += item["despesa_variavel"]
            despesa_fixa += item["despesa_fixa"]
            comissao += item["comissao"]
            negativo += item["lucro_rs"] if item["lucro_rs"] < 0 else 0.00
            lucro_rs += item["lucro_rs"]

        if lucro_rs != 0:
            lucro_percentual += round((lucro_rs / faturamento) * 100, 3)

        return {
            "faturamento": round(faturamento, 2),
            "custo": round(custo, 2),
            "despesa_variavel": round(despesa_variavel, 2),
            "despesa_fixa": round(despesa_fixa, 2),
            "comissao": round(comissao, 2),
            "negativo": round(negativo, 2),
            "lucro_rs": round(lucro_rs, 2),
            "lucro_percentual": lucro_percentual
        }


if __name__ == "__main__":
    dados = FaturamentoBusiness()

    print(dados.dados_venda_item)
