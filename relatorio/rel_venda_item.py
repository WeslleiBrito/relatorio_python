from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import Paragraph, Table, TableStyle
from reportlab.lib.styles import ParagraphStyle
from datetime import date
from business.faturamento.faturamento_business import FaturamentoBusiness
import locale

locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')


class RelatorioItem:
    def __init__(self, data_inicial: str = "", data_final: str = "", comissao: float = 1):
        self.__data_inicial = data_inicial
        self.__data_final = data_final
        self.__comissao = comissao
        self.__dados = FaturamentoBusiness(data_inicial=self.__data_inicial, data_final=self.__data_final,
                                           comissao=self.__comissao)
        self.__pdf = canvas.Canvas(f"LUCRATIVIDADE_{date.today()}.pdf", pagesize=A4)
        # Definir margens e espaçamentos
        self.top_margin_first_page = 700  # Espaço reservado para o cabeçalho na primeira página
        self.top_margin_other_pages = 750  # Pequeno espaço nas páginas subsequentes
        self.left_margin = 20
        self.bottom_margin = 50  # Margem inferior da tabela
        
        self.__cabecalho = [
            Paragraph('Venda', self.__style_paragraph()),
            Paragraph('Qtd', self.__style_paragraph()),
            Paragraph('Descrição', self.__style_paragraph()),
            Paragraph('Fat.', self.__style_paragraph()),
            Paragraph('Custo', self.__style_paragraph()),
            Paragraph('Comissão', self.__style_paragraph()),
            Paragraph('D. Variável', self.__style_paragraph()),
            Paragraph('D. Fixa', self.__style_paragraph()),
            Paragraph('Custo + Despesa', self.__style_paragraph()),
            Paragraph('Lucro R$', self.__style_paragraph()),
            Paragraph('Lucro %', self.__style_paragraph())
        ]
        self.__tamanho_colunas = [
            35,
            50,
            130,
            60,
            40,
            30,
            40,
            40,
            50,
            40
        ]

    def relatorio(self):
        self.__relatorio_faturamento_item()
    
    def gerar_cabecalho_primeira_pagina(self):
        # Cabeçalho com informações no topo da primeira página
        self.__pdf.drawString(100, 800, "Relatório de Lucratividade")
        self.__pdf.drawString(100, 780, f"Data: {date.today()}")
        self.__pdf.drawString(100, 760, "Período: 01/01/2024 a 31/12/2024")
        
    def __relatorio_faturamento_item(self):
        lista_dados = [list(item.values())[1:] for item in self.__dados.dados_venda_item]

        lista_formatada = []

        for index, item in enumerate(lista_dados):
            venda = Paragraph(str(item[0]), self.__style_paragraph())
            quantidade = Paragraph(locale.format_string('%.2f', item[2], grouping=True), self.__style_paragraph())
            descricao = Paragraph(item[3], self.__style_paragraph())
            faturamento = Paragraph(locale.format_string('%.2f', item[4], grouping=True), self.__style_paragraph())
            custo = Paragraph(locale.format_string('%.2f', item[5], grouping=True), self.__style_paragraph())
            comissao = Paragraph(locale.format_string('%.2f', item[6], grouping=True), self.__style_paragraph())
            despesa_variavel = Paragraph(locale.format_string('%.2f', item[7], grouping=True), self.__style_paragraph())
            despesa_fixa = Paragraph(locale.format_string('%.2f', item[8], grouping=True), self.__style_paragraph())
            custo_despesa = Paragraph(locale.format_string('%.2f', item[10], grouping=True), self.__style_paragraph())
            lucro_rs = Paragraph(locale.format_string('%.2f', item[11], grouping=True),
                                 self.__style_paragraph(item[11]))
            lucro_porcentagem = Paragraph(locale.format_string('%.2f', item[12] * 100, grouping=True),
                                          self.__style_paragraph(item[12]))

            lista_formatada.append([
                venda,
                quantidade,
                descricao,
                faturamento,
                custo,
                comissao,
                despesa_variavel,
                despesa_fixa,
                custo_despesa,
                lucro_rs,
                lucro_porcentagem
            ])

        lista_formatada.insert(0, self.__cabecalho)
        table = Table(
            lista_formatada,
            colWidths=self.__tamanho_colunas
        )
        estilo_tabela = TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                                   ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                                   ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                   ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                                   ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                                   ('FONTSIZE', (0, 0), (-1, 0), 10),
                                   ('FONTSIZE', (0, 1), (-1, -1), 7),
                                   ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                                   ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                                   ('GRID', (0, 0), (-1, -1), 1, colors.black)])
        table.setStyle(estilo_tabela)

        available_width, available_height = A4

        # Desenhar na primeira página com cabeçalho
        pos_y = self.top_margin_first_page  # Começa a tabela mais abaixo na primeira página
        self.gerar_cabecalho_primeira_pagina()  # Inserir o cabeçalho na primeira página

        # Verificar se a tabela cabe na página
        required_width, required_height = table.wrap(available_width, available_height)

        # Variável para rastrear a tabela restante
        remaining_table = table

        if required_height <= (pos_y - self.bottom_margin):
            # Se a tabela cabe na primeira página
            tabela.wrapOn(self.__pdf, available_width, available_height)
            tabela.drawOn(self.__pdf, self.left_margin, pos_y - required_height)
        else:
            # Dividir a tabela em partes que caibam na página sem cortar linhas
            is_first_page = True

            while remaining_table and remaining_table._cellvalues:
                if is_first_page:
                    pos_y = self.top_margin_first_page  # Margem superior da primeira página
                    is_first_page = False
                else:
                    pos_y = self.top_margin_other_pages  # Menor margem nas páginas seguintes

                available_height = pos_y - self.bottom_margin

                # Verifica quantas linhas da tabela cabem na página sem cortar
                part_height = 0
                table_parts = []
                for row in remaining_table._cellvalues:
                    # Criar uma tabela temporária com as linhas atuais
                    temp_table = Table([row], colWidths=self.__tamanho_colunas)
                    row_width, row_height = temp_table.wrap(available_width, available_height)

                    # Se a linha ultrapassar o espaço disponível, parar e passar para a próxima página
                    if part_height + row_height > available_height:
                        break

                    table_parts.append(row)
                    part_height += row_height

                # Criar tabela com as partes que cabem na página
                part = Table(table_parts, colWidths=self.__tamanho_colunas)
                part.setStyle(estilo_tabela)  # Aplicar o estilo da tabela original

                # Desenhar a parte atual da tabela
                part.wrapOn(self.__pdf, available_width, available_height)
                part.drawOn(self.__pdf, self.left_margin, pos_y - part_height)

                # Se ainda houver linhas restantes, atualize a tabela restante
                if len(table_parts) < len(remaining_table._cellvalues):
                    remaining_table = Table(remaining_table._cellvalues[len(table_parts):],
                                            colWidths=self.__tamanho_colunas)
                    remaining_table.setStyle(estilo_tabela)
                else:
                    remaining_table = None  # Todas as linhas foram desenhadas

                # Criar nova página se ainda houver linhas para desenhar
                if remaining_table and remaining_table._cellvalues:
                    self.__pdf.showPage()  # Criar uma nova página

        self.__pdf.save()

    @staticmethod
    def __style_paragraph(numero: float = None):
        if numero:
            return ParagraphStyle(
                'CustomStyle',
                fontName='Helvetica-Bold',
                fontSize=7,
                textColor=colors.black if numero > 0 else colors.red if numero == 0 else colors.yellow,
                alignment=1,  # Centralizado (TA_CENTER)
                spaceBefore=0,  # Espaçamento antes do parágrafo
                spaceAfter=3,  # Espaçamento depois do parágrafo
                leading=8.5
            )

        return ParagraphStyle(
            'CustomStyle',
            fontName='Helvetica-Bold',
            fontSize=7,
            textColor=colors.black,
            alignment=1,  # Centralizado (TA_CENTER)
            spaceBefore=0,  # Espaçamento antes do parágrafo
            spaceAfter=3,  # Espaçamento depois do parágrafo
            leading=8.5
        )


if __name__ == '__main__':
    busca = RelatorioItem(data_inicial="2024-09-01", data_final="2024-09-23")
    busca.relatorio()
