from database.faturamento_database.faturamento_database import FaturamentoDatabase
from ferramentas.ferramentas import extrair_primeiros_nomes
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle, Paragraph
from reportlab.lib.units import cm
from reportlab.lib.styles import ParagraphStyle
from datetime import date
import locale

locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')


class RelatorioItem:
    def __init__(self, data_inicial: str = "", data_final: str = "", comissao: float = 1):
        self.__data_inicial = data_inicial
        self.__data_final = data_final
        self.__comissao = comissao
        self.__dados = FaturamentoDatabase(data_inicial=self.__data_inicial, data_final=self.__data_final,
                                           comissao=self.__comissao)
        self.__pdf = canvas.Canvas(f"LUCRATIVIDADE-{date.today()}", pagesize=A4)
        self.__custom_style = ParagraphStyle(
            'CustomStyle',
            fontName='Helvetica-Bold',
            fontSize=8,
            textColor=colors.black,
            alignment=1,  # Centralizado (TA_CENTER)
            spaceBefore=0,  # Espaçamento antes do parágrafo
            spaceAfter=3,  # Espaçamento depois do parágrafo
            leading=8.5
        )
        self.__cabecalho = [
            Paragraph('Venda', self.__custom_style),
            Paragraph('Vendedor', self.__custom_style),
            Paragraph('Qtd', self.__custom_style),
            Paragraph('Descrição', self.__custom_style),
            Paragraph('Fat.', self.__custom_style),
            Paragraph('Custo', self.__custom_style),
            Paragraph('Comissão', self.__custom_style),
            Paragraph('Despesa Variável', self.__custom_style),
            Paragraph('Despesa Fixa', self.__custom_style),
            Paragraph('Lucro R$', self.__custom_style),
            Paragraph('Lucro %', self.__custom_style)
        ]
        self.__tamanho_colunas = [
            50,
            75,
            50,
            170,
            60,
            40,
            40,
            50,
            50,
            50
        ]

    @property
    def relatorio(self):
        return self.__relatorio_faturamento_item()

    def __relatorio_faturamento_item(self):
        lista_dados = [list(item.values())[1:-1] for item in self.__dados.busca_venda_item]
        lista_formatada = []
        for index, item in enumerate(lista_dados):
            venda = Paragraph(item[0], self.__custom_style)
            vendedor = Paragraph(extrair_primeiros_nomes(item[1]), self.__custom_style)
            quantidade = Paragraph(locale.format_string('%.2f', item[2], grouping=True), self.__custom_style)
        return lista_dados


if __name__ == '__main__':
    busca = RelatorioItem()
    for produto in busca.relatorio:
        print(produto)
