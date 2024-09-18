import mysql.connector
from connect_database import conecta_banco
from typing import TypedDict, List


class InterfaceSubgrupoBasica(TypedDict):
    codigo: int
    descricao: str
    despesa_fixa: float


class InterfaceSubgrupoCompleta(InterfaceSubgrupoBasica):
    quantidade: float
    quantidade_devolvida: float
    faturamento: float
    custo: float


class Subgrupo:

    def __init__(self, host_name="servidorBalcao"):
        self.conn = conecta_banco(host_name)

    @property
    def dados_basicos(self):
        return self.__busca_dados_basicos()

    def __busca_dados_completo(self) -> List[InterfaceSubgrupoBasica]:
        cursor = None
        try:
            cursor = self.conn.cursor(dictionary=True)

            query = """
                SELECT cod_subgroup AS "codigo", name_subgroup AS "descricao", fixed_unit_expense AS "despesa_fixa" 
                FROM resume_subgroups
            """

            cursor.execute(query)

            resultados: List[InterfaceSubgrupoBasica] = cursor.fetchall()

            return [
                {"codigo": item['codigo'], "descricao": item['descricao'], "despesa_fixa": float(item["despesa_fixa"])}
                for item in resultados]

        except mysql.connector.Error as err:
            print(f"Erro ao acessar o banco de dados: {err}")
        finally:
            if cursor is not None:
                cursor.close()
                self.conn.close()

    def __busca_dados_basicos(self) -> List[InterfaceSubgrupoBasica]:
        cursor = None
        try:
            cursor = self.conn.cursor(dictionary=True)

            query = """
                SELECT cod_subgroup AS "codigo", name_subgroup AS "descricao", fixed_unit_expense AS "despesa_fixa" 
                FROM resume_subgroups
            """

            cursor.execute(query)

            resultados: List[InterfaceSubgrupoBasica] = cursor.fetchall()

            return [
                {"codigo": item['codigo'], "descricao": item['descricao'], "despesa_fixa": float(item["despesa_fixa"])}
                for item in resultados]

        except mysql.connector.Error as err:
            print(f"Erro ao acessar o banco de dados: {err}")
        finally:
            if cursor is not None:
                cursor.close()
                self.conn.close()


if __name__ == "__main__":
    busca = Subgrupo()
    for data in busca.dados_basicos:
        print(data)
