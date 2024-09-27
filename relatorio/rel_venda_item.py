import os
import sys
import locale
from datetime import date
from reportlab.lib.pagesizes import A4, letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import Paragraph, Table, TableStyle, Spacer, BaseDocTemplate, Frame, PageTemplate, KeepTogether
from reportlab.lib.styles import ParagraphStyle

# Adicionando o caminho do projeto dinamicamente
BASE_DIR = os.path.abspath(r"C:\Users\Wesllei\PycharmProjects\modelo_relatorio_teste")
sys.path.append(BASE_DIR)
from business.faturamento.faturamento_business import FaturamentoBusiness
from ferramentas.Print.print import Print

# Configuração de Paths via Variáveis de Ambiente (opcional)
PDF_OUTPUT_DIR = os.getenv('PDF_OUTPUT_DIR', os.path.join(BASE_DIR, "relatorio"))
if not os.path.exists(PDF_OUTPUT_DIR):
    os.makedirs(PDF_OUTPUT_DIR)

# Configuração do Locale
try:
    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
except locale.Error as e:
    print(f"Erro ao configurar locale: {e}")
    locale.setlocale(locale.LC_ALL, '')  # Fallback para locale padrão


def define_styles():
    """Define os estilos utilizados no relatório."""
    styles = {
        'header': ParagraphStyle(
            'HeaderStyle',
            fontName='Helvetica-Bold',
            fontSize=6,
            textColor=colors.whitesmoke,
            alignment=1,  # Centralizado
            spaceBefore=0,
            spaceAfter=3,
            leading=12,
            backColor=colors.grey
        ),
        'default': ParagraphStyle(
            'DefaultStyle',
            fontName='Helvetica-Bold',
            fontSize=6,
            textColor=colors.black,
            alignment=1,  # Centralizado
            spaceBefore=0,
            spaceAfter=3,
            leading=8.5
        )
    }
    return styles


def _style_lucro(numero: float):
    """Define o estilo de acordo com o valor do lucro."""
    if numero is not None:
        if numero > 0:
            color = colors.green
        elif numero < 0:
            color = colors.red
        else:
            color = colors.yellow
    else:
        color = colors.black

    return ParagraphStyle(
        'LucroStyle',
        fontName='Helvetica-Bold',
        fontSize=7,
        textColor=color,
        alignment=1,  # Centralizado
        spaceBefore=0,
        spaceAfter=3,
        leading=8.5
    )


class RelatorioItem:
    def __init__(self, data_inicial: str = "", data_final: str = "", comissao: float = 1, file_path: str = "",
                 print_rel: bool = False, printer_name=None):
        self.print_rel = print_rel
        self.printer_name = printer_name
        self.data_inicial = data_inicial
        self.data_final = data_final
        self.comissao = comissao
        self.dados_completos = FaturamentoBusiness(
            data_inicial=self.data_inicial,
            data_final=self.data_final,
            comissao=self.comissao
        )
        self.dados = self.dados_completos.dados_venda_item["dados_unitarios"]
        self.resumo = self.dados_completos.dados_venda_item["resumo"]
        self.apuracao_i = self.dados_completos.dados_venda_item["periodo_apuracao"]["data_inicial"]
        self.apuracao_f = self.dados_completos.dados_venda_item["periodo_apuracao"]["data_final"]

        if file_path:
            self.path = os.path.join(
                file_path,
                f"lucratividade_{self.apuracao_i.replace('/', '_')}_A_{self.apuracao_f.replace('/', '_')}.pdf"
            )
        else:
            self.path = os.path.join(
                PDF_OUTPUT_DIR,
                f"lucratividade_{self.apuracao_i.replace('/', '_')}_A_{self.apuracao_f.replace('/', '_')}.pdf"
            )

        self.page_width, self.page_height = A4

        # Definir margens fixas
        self.top_margin = 50  # Margem superior fixa
        self.bottom_margin = 20  # Margem inferior fixa
        self.left_margin = 20  # Margem esquerda fixa
        self.right_margin = 20  # Margem direita fixa

        # Espaçamentos
        self.space_between_header_and_table = 50
        self.space_between_table_and_summary = 30

        # Definir estilos
        self.styles = define_styles()

        # Cabeçalho da tabela
        self.cabecalho = [
            Paragraph('Venda', self.styles['header']),
            Paragraph('Qtd', self.styles['header']),
            Paragraph('Descrição', self.styles['header']),
            Paragraph('Faturamento', self.styles['header']),
            Paragraph('Custo', self.styles['header']),
            Paragraph('Comissão', self.styles['header']),
            Paragraph('Despesa Variável', self.styles['header']),
            Paragraph('Despesa Fixa', self.styles['header']),
            Paragraph('Custo + Despesa', self.styles['header']),
            Paragraph('Lucro R$', self.styles['header']),
            Paragraph('Lucro %', self.styles['header'])
        ]
        self.tamanho_colunas = [
            35,
            50,
            130,
            60,
            40,
            30,
            40,
            40,
            50,
            40,
            40
        ]

    def relatorio(self):
        """Método principal para gerar o relatório."""
        try:
            self.__relatorio_faturamento_item()
            if self.print_rel:
                self.__imprimir_relatorio()
            print(f"Relatório gerado com sucesso: {self.path}")
        except Exception as e:
            print(f"Erro ao gerar o relatório: {e}")

    def __imprimir_relatorio(self):
        """Método para imprimir o relatório PDF."""
        try:
            Print(self.path, self.printer_name).print_pdf()
            print("Relatório enviado para a impressora com sucesso.")
        except Exception as e:
            print(f"Erro ao imprimir o relatório: {e}")

    def __relatorio_faturamento_item(self):
        """Gera a tabela de faturamento por item no PDF."""
        # Preparar os dados da tabela
        lista_dados = [list(item.values())[1:] for item in self.dados]
        lista_formatada = []

        for item in lista_dados:
            venda = Paragraph(str(item[0]), self.styles['default'])
            quantidade = Paragraph(locale.format_string('%.2f', item[2], grouping=True), self.styles['default'])
            descricao = Paragraph(item[3], self.styles['default'])
            faturamento = Paragraph(locale.format_string('%.2f', item[4], grouping=True), self.styles['default'])
            custo = Paragraph(locale.format_string('%.2f', item[5], grouping=True), self.styles['default'])
            comissao = Paragraph(locale.format_string('%.2f', item[6], grouping=True), self.styles['default'])
            despesa_variavel = Paragraph(locale.format_string('%.2f', item[7], grouping=True), self.styles['default'])
            despesa_fixa = Paragraph(locale.format_string('%.2f', item[8], grouping=True), self.styles['default'])
            custo_despesa = Paragraph(locale.format_string('%.2f', item[10], grouping=True), self.styles['default'])
            lucro_rs = Paragraph(locale.format_string('%.2f', item[11], grouping=True), _style_lucro(item[11]))
            lucro_porcentagem = Paragraph(locale.format_string('%.2f', item[12] * 100, grouping=True),
                                          _style_lucro(item[12]))

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

        lista_formatada.insert(0, self.cabecalho)  # Inserir o cabeçalho no topo da tabela
        table = Table(lista_formatada, colWidths=self.tamanho_colunas, repeatRows=1)

        # Estilos para a tabela principal
        estilo_tabela = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('FONTSIZE', (0, 1), (-1, -1), 7),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.black)
        ])
        table.setStyle(estilo_tabela)

        # Criar a tabela de resumo
        resumo_table = self.__create_resumo()

        # Envolver a tabela de resumo em KeepTogether para evitar divisão entre páginas
        resumo_keep_together = KeepTogether([resumo_table])

        # Definir o layout do documento usando Platypus
        doc = BaseDocTemplate(
            self.path,
            pagesize=A4,
            rightMargin=self.right_margin,
            leftMargin=self.left_margin,
            topMargin=self.top_margin,
            bottomMargin=self.bottom_margin
        )

        # Definir frames para as páginas
        frame = Frame(
            doc.leftMargin,
            doc.bottomMargin,
            doc.width,
            doc.height,
            id='normal'
        )

        # Definir o template de página com cabeçalho
        template = PageTemplate(id='test', frames=frame, onPage=self.__add_page_header)
        doc.addPageTemplates([template])

        # Construir a história (story)
        story = [
            Spacer(1, self.space_between_header_and_table),
            table,
            Spacer(1, self.space_between_table_and_summary),
            Spacer(100, 0),  # Adiciona espaço horizontal para mover o resumo à direita
            resumo_keep_together
        ]

        # Construir o documento
        try:
            doc.build(story)
        except Exception as e:
            print(f"Erro ao construir o documento: {e}")

    def __create_resumo(self):
        """Cria a tabela de resumo."""
        resumo_dados = [
            ["Faturamento", locale.format_string('%.2f', self.resumo["faturamento"], grouping=True)],
            ["Custo", locale.format_string('%.2f', self.resumo["custo"], grouping=True)],
            ["Despesa Fixa", locale.format_string('%.2f', self.resumo["despesa_fixa"], grouping=True)],
            ["Despesa Variável", locale.format_string('%.2f', self.resumo["despesa_variavel"], grouping=True)],
            ["Comissão", locale.format_string('%.2f', self.resumo["comissao"], grouping=True)],
            ["Negativo", locale.format_string('%.2f', self.resumo["negativo"], grouping=True)],
            ["Lucro R$", locale.format_string('%.2f', self.resumo["lucro_rs"], grouping=True)],
            ["Lucro %", locale.format_string('%.2f', self.resumo["lucro_percentual"], grouping=True)],
        ]

        # Definir a largura da tabela
        col_widths = [100, 80]  # Ajuste conforme necessário
        resumo_table = Table(resumo_dados, colWidths=col_widths)

        # Aplicar estilo à tabela
        estilo_resumo = TableStyle([
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.black)
        ])
        resumo_table.setStyle(estilo_resumo)

        return resumo_table

    def __add_page_header(self, canvas_obj, doc):
        """Adiciona o cabeçalho e rodapé com número de página em todas as páginas."""
        canvas_obj.saveState()

        # Cabeçalho
        if doc.page == 1:
            # Cabeçalho da primeira página
            canvas_obj.setFont("Helvetica-Bold", 16)
            canvas_obj.drawString(self.left_margin, self.page_height - self.top_margin + 20,
                                  "Relatório de Lucratividade")
            canvas_obj.setFont("Helvetica", 10)
            canvas_obj.drawString(self.left_margin, self.page_height - self.top_margin,
                                  f"Data: {date.today().strftime('%d/%m/%Y')}")
            canvas_obj.drawString(self.left_margin, self.page_height - self.top_margin - 20,
                                  f"Período: {self.apuracao_i} a {self.apuracao_f}")

        # Rodapé com número da página
        canvas_obj.setFont("Helvetica", 9)
        page_number_text = f"Página {doc.page}"
        canvas_obj.drawRightString(self.page_width - self.right_margin, self.bottom_margin - 10, page_number_text)

        canvas_obj.restoreState()


if __name__ == '__main__':
    try:
        busca = RelatorioItem(file_path=r"C:\Automatizacao\Lucratividade")
        busca.relatorio()
    except Exception as e:
        print(f"Erro ao executar o script: {e}")
