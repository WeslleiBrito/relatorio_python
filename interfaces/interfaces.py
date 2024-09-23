from typing import TypedDict
from datetime import datetime, date


class InterfaceSubgrupoBasica(TypedDict):
    codigo: int
    descricao: str
    despesa_fixa: float


class InterfaceSubgrupoCompleta(InterfaceSubgrupoBasica):
    quantidade: float
    quantidade_devolvida: float
    faturamento: float
    custo: float
    desconto: float
    total_despesa_fixa: float
    total_despesa_variavel: float
    porcentagem_lucro: float
    total_lucro: float
    porcentagem_desconto: float
    porcentagem_faturamento: float
    porcentagem_custo: float
    porcentagem_despesa_fixa: float
    data_criacao: datetime
    data_atualizacao: datetime


class InterfaceFaturamento(TypedDict):
    codigo: int
    venda: int
    vendedor: str
    quantidade: float
    descricao: str
    custo: float
    faturamento: float
    comissao: float
    despesa_fixa: float
    despesa_variavel: float
    data_venda: date


class InterfaceFaturamentoItem(InterfaceFaturamento):
    custo_despesa: float
    lucro_rs: float
    lucro_porcentagem: float


class InterfaceValoresGlobal(TypedDict):
    id: str
    invoicing: float
    cost: float
    fixed_expenses: float
    variable_expenses: float
    created_at: datetime
    updated_at: datetime
    discount: float
    discount_percentage: float
    variable_expense_percentage: float
    general_monetary_profit: float
    general_percentage_profit: float
    number_of_months: int
