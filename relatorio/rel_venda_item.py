from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import Paragraph, Table, TableStyle
from reportlab.lib.styles import ParagraphStyle
from datetime import date
from business.faturamento.faturamento_business import FaturamentoBusiness
from ferramentas.Print.print import Print
import locale

locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')


class RelatorioItem:
    def __init__(self, data_inicial: str = "", data_final: str = "", comissao: float = 1, file_path: str = "",
                 print_rel: bool = False, printer_name=None):
        self.__print_rel = print_rel
        self.__printer_name = printer_name
        self.__data_inicial = data_inicial
        self.__data_final = data_final
        self.__comissao = comissao
        self.__dados_completos = FaturamentoBusiness(data_inicial=self.__data_inicial, data_final=self.__data_final,
                                                     comissao=self.__comissao)
        self.__dados = self.__dados_completos.dados_venda_item["dados_unitarios"]
        self.__resumo = self.__dados_completos.dados_venda_item["resumo"]
        self.__apuracao_i = self.__dados_completos.dados_venda_item["periodo_apuracao"]["data_inicial"]
        self.__apuracao_f = self.__dados_completos.dados_venda_item["periodo_apuracao"]["data_final"]
        if file_path:
            self.__path = (f"{file_path}\lucratividade_{self.__apuracao_i.replace('/', '_')}_A_"
                           f"{self.__apuracao_f.replace('/', '_')}.pdf")
        else:
            self.__path = (rf"C:\Users\Wesllei\PycharmProjects\modelo_relatorio_teste\relatorio\lucratividade_"
                           rf"{self.__apuracao_i.replace('/', '_')}_A_"
                           f"{self.__apuracao_f.replace('/', '_')}.pdf")

        self.__pdf = canvas.Canvas(self.__path, pagesize=A4)

        # Definir margens e espaçamentos
        self.top_margin_first_page = 730  # Espaço reservado para o cabeçalho na primeira página
        self.top_margin_other_pages = 800  # Pequeno espaço nas páginas subsequentes
        self.left_margin = 20
        self.bottom_margin = 20  # Margem inferior da tabela
        self.__space_between_table_and_summary = 30
        self.__margin_x_resumo = 320

        self.__cabecalho = [
            Paragraph('Venda', self.__style_paragraph()),
            Paragraph('Qtd', self.__style_paragraph()),
            Paragraph('Descrição', self.__style_paragraph()),
            Paragraph('Faturamento', self.__style_paragraph()),
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
        self.__pdf.drawString(20, 800, "Relatório de Lucratividade")
        self.__pdf.drawString(20, 780, f"Data: {date.today().strftime('%d/%m/%Y')}")
        self.__pdf.drawString(20, 760, f"Período: {self.__apuracao_i} a {self.__apuracao_f}")

    def __relatorio_faturamento_item(self):
        lista_dados = [list(item.values())[1:] for item in self.__dados]
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

        lista_formatada.insert(0, self.__cabecalho)  # Inserir o cabeçalho no topo da tabela
        table = Table(lista_formatada, colWidths=self.__tamanho_colunas)

        # Aplicando estilos para a tabela principal, incluindo o cabeçalho destacado
        estilo_tabela_primeira_pagina = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),  # Cor de fundo para o cabeçalho
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),  # Cor do texto do cabeçalho
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('FONTSIZE', (0, 1), (-1, -1), 7),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),  # Cor para as linhas de dados
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ])

        estilo_tabela_outras_paginas = TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('FONTSIZE', (0, 0), (-1, -1), 7),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 0), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ])

        # Desenhar a tabela de vendas
        available_width, available_height = A4
        pos_y = self.top_margin_first_page  # Para a primeira página
        self.gerar_cabecalho_primeira_pagina()

        required_width, required_height = table.wrap(available_width, available_height)

        # Inicializar remaining_table com a tabela completa
        remaining_table = table

        # Desenhar a tabela de vendas
        if required_height <= (pos_y - self.bottom_margin):
            table.setStyle(estilo_tabela_primeira_pagina)
            table.wrapOn(self.__pdf, available_width, available_height)
            table.drawOn(self.__pdf, self.left_margin, pos_y - required_height)
            pos_y -= required_height  # Atualizar a posição Y para a página atual

        else:
            page = 1
            # Lógica para desenhar a tabela em várias páginas
            while remaining_table and remaining_table.cellvalues:  # Certifique-se de usar _cellvalues
                available_height = pos_y - self.bottom_margin

                # Dividir a tabela em partes que caibam na página
                part_height = 0
                table_parts = []
                for row in remaining_table.cellvalues:
                    temp_table = Table([row], colWidths=self.__tamanho_colunas)
                    row_width, row_height = temp_table.wrap(available_width, available_height)

                    # Verificar se cabe na página atual
                    if part_height + row_height > available_height:
                        break
                    table_parts.append(row)
                    part_height += row_height

                # Desenhar parte da tabela
                part = Table(table_parts, colWidths=self.__tamanho_colunas)

                if page == 1:
                    part.setStyle(estilo_tabela_primeira_pagina)
                else:
                    part.setStyle(estilo_tabela_outras_paginas)  # Aplicando o estilo para outras páginas

                page += 1

                part.wrapOn(self.__pdf, available_width, available_height)
                part.drawOn(self.__pdf, self.left_margin, pos_y - part_height)

                pos_y -= part_height  # Atualiza a posição Y na página

                # Atualizar a tabela restante
                if len(table_parts) < len(remaining_table.cellvalues):
                    remaining_table = Table(remaining_table.cellvalues[len(table_parts):],
                                            colWidths=self.__tamanho_colunas)
                else:
                    remaining_table = None

                # Se precisar de nova página, cria uma nova
                if remaining_table:
                    self.__pdf.showPage()
                    pos_y = self.top_margin_other_pages

        # Tabela de resumo
        resumo_dados = [
            ["Faturamento", locale.format_string('%.2f', self.__resumo["faturamento"], grouping=True)],
            ["Custo", locale.format_string('%.2f', self.__resumo["custo"], grouping=True)],
            ["Despesa Fixa", locale.format_string('%.2f', self.__resumo["despesa_fixa"], grouping=True)],
            ["Despesa Variável", locale.format_string('%.2f', self.__resumo["despesa_variavel"], grouping=True)],
            ["Comissão", locale.format_string('%.2f', self.__resumo["comissao"], grouping=True)],
            ["Negativo", locale.format_string('%.2f', self.__resumo["negativo"], grouping=True)],
            ["Lucro R$", locale.format_string('%.2f', self.__resumo["lucro_rs"], grouping=True)],
            ["Lucro %", locale.format_string('%.2f', self.__resumo["lucro_percentual"], grouping=True)],
        ]
        resumo_table = Table(resumo_dados, colWidths=[100, 100])

        # Aplicando estilo à tabela de resumo
        estilo_resumo = TableStyle([
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ])
        resumo_table.setStyle(estilo_resumo)

        # Espaço necessário para o resumo
        resumo_width, resumo_height = resumo_table.wrap(available_width, available_height)

        # Verificar se há espaço para o resumo na última página (somente nela)
        if (pos_y - (resumo_height + 30) - self.bottom_margin) > self.bottom_margin:
            # Se houver espaço, desenha o resumo
            pos_y -= (self.__space_between_table_and_summary + (resumo_height + 30))
            resumo_table.wrapOn(self.__pdf, available_width, available_height)
            resumo_table.drawOn(self.__pdf, self.left_margin + self.__margin_x_resumo, pos_y)
        else:
            # Caso contrário, cria uma nova página para o resumo
            self.__pdf.showPage()
            pos_y = self.top_margin_other_pages
            resumo_table.wrapOn(self.__pdf, available_width, available_height)
            resumo_table.drawOn(self.__pdf, self.left_margin + self.__margin_x_resumo, pos_y - (resumo_height + 30))

        self.__pdf.save()
        if self.__print_rel:
            Print(self.__path, self.__printer_name).print_pdf()

    @staticmethod
    def __style_paragraph(numero: float = None):
        if numero:
            color = colors.black
            if numero == 0:
                color = colors.yellow
            elif numero < 0:
                color = colors.red

            return ParagraphStyle(
                'CustomStyle',
                fontName='Helvetica-Bold',
                fontSize=7,
                textColor=color,
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
    busca = RelatorioItem(file_path=r"C:\Automatizacao\Lucratividade", print_rel=True)
    busca.relatorio()
