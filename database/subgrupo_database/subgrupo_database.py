import mysql.connector
from database.connect_database import conecta_banco


class SubgrupoDatabase:

    def __init__(self, host_name="servidorBalcao"):
        self.__conn = conecta_banco(host_name)

    def busca_dados(self, full: bool = False):
        cursor = None
        try:
            cursor = self.__conn.cursor(dictionary=True)

            query_simple = """
                SELECT
                    resume_subgroups.cod_subgroup AS codigo,
                    subgrupo_produtos.subprod_descricao AS descricao,
                    subgrupo_produtos.plucro AS lucro_subgrupo_padrao,
                    resume_subgroups.fixed_unit_expense AS despesa_fixa
                FROM
                    resume_subgroups
                INNER JOIN subgrupo_produtos ON subgrupo_produtos.subprod_cod = resume_subgroups.cod_subgroup
            """
            query_all = """
                SELECT
                    resume_subgroups.cod_subgroup AS codigo,
                    subgrupo_produtos.subprod_descricao AS descricao,
                    subgrupo_produtos.plucro AS lucro_subgrupo_padrao,
                    resume_subgroups.amount_quantity AS quantidade,
                    resume_subgroups.amount_quantity_returned AS quantidade_devolvida,
                    resume_subgroups.amount_invoicing AS faturamento,
                    resume_subgroups.amount_cost AS custo,
                    resume_subgroups.amount_discount AS desconto,
                    resume_subgroups.amount_fixed AS total_despesa_fixa,
                    resume_subgroups.amount_variable AS total_despesa_variavel,
                    resume_subgroups.fixed_unit_expense AS despesa_fixa,
                    resume_subgroups.plucro AS porcentagem_lucro,
                    resume_subgroups.subgroup_profit AS total_lucro,
                    resume_subgroups.discount_percentage AS porcentagem_desconto,
                    resume_subgroups.invoicing_percentage AS porcentagem_faturamento,
                    resume_subgroups.cost_percentage AS porcentagem_custo,
                    resume_subgroups.fixed_expense_percentage AS porcentagem_despesa_fixa,
                    resume_subgroups.subgroup_profit_percentage AS porcentagem_lucro,
                    resume_subgroups.created_at AS data_criacao,
                    resume_subgroups.updated_at AS data_atualizacao
                FROM
                    resume_subgroups
                INNER JOIN subgrupo_produtos ON subgrupo_produtos.subprod_cod = resume_subgroups.cod_subgroup

            """

            cursor.execute(query_all if full else query_simple)

            return cursor.fetchall()

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
