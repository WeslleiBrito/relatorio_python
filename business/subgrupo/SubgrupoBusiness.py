from database.subgrupo_database.subgrupo_database import SubgrupoDatabase
from typing import List, cast
from interfaces.interfaces import InterfaceSubgrupoBasica, InterfaceSubgrupoCompleta


class SubgrupoBusiness:
    def __init__(self):
        self.__subgrupo_database = SubgrupoDatabase()

    @property
    def busca_completa(self) -> List[InterfaceSubgrupoCompleta]:
        return self.__busca_completa_subgrupo()

    @property
    def busca_simples(self) -> List[InterfaceSubgrupoBasica]:
        return self.__busca_simples_subgrupo()

    def __busca_completa_subgrupo(self) -> List[InterfaceSubgrupoCompleta]:
        resultado = self.__subgrupo_database.busca_dados(full=True)

        return [
            cast(InterfaceSubgrupoCompleta, {
                "codigo": item["codigo"],
                "descricao": item["descricao"],
                "lucro_subgrupo_padrao": item["lucro_subgrupo_padrao"],
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

    def __busca_simples_subgrupo(self) -> List[InterfaceSubgrupoBasica]:
        resultado = self.__subgrupo_database.busca_dados()

        return [
            cast(InterfaceSubgrupoBasica, {
                "codigo": item["codigo"],
                "descricao": item["descricao"],
                "lucro_subgrupo_padrao": item["lucro_subgrupo_padrao"],
                "despesa_fixa": float(item["despesa_fixa"])
            })
            for item in resultado
        ]


if __name__ == "__main__":
    busca = SubgrupoBusiness()

    for subgrupo in busca.busca_simples:
        print(subgrupo)
