from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle, Paragraph
from reportlab.lib.units import cm
from reportlab.lib.styles import ParagraphStyle
import locale

locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

# Criar o canvas (superfície de desenho) e definir o tamanho do papel
pdf = canvas.Canvas("exemplo.pdf", pagesize=A4)

# Definir a fonte e tamanho para o texto
pdf.setFont("Helvetica", 12)

custom_style = ParagraphStyle(
    'CustomStyle',
    fontName='Helvetica-Bold',
    fontSize=8,
    textColor=colors.black,
    alignment=1,  # Centralizado (TA_CENTER)
    spaceBefore=0,  # Espaçamento antes do parágrafo
    spaceAfter=3,  # Espaçamento depois do parágrafo
    leading=8.5
)

# Adicionar um texto ao PDF
pdf.drawString(100, 800, "Relatório Gerado com ReportLab")
tamanho_colunas = [
    50,
    75,
    50,
    170,
    50,
    60,
    50,
    50
]

cabecalho = [
    Paragraph('Venda', custom_style),
    Paragraph('Vendedor', custom_style),
    Paragraph('Qtd', custom_style),
    Paragraph('Descrição', custom_style),
    Paragraph('Custo', custom_style),
    Paragraph('Fat.', custom_style),
    Paragraph('Lucro R$', custom_style),
    Paragraph('Lucro %', custom_style)
]

# Inserir uma tabela no PDF

datas = [
         ['001', 'João Silva', 10,
          'Teclado Mecânico, Teclado Mecânico, Teclado Mecânico, Teclado Mecânico, Teclado Mecânico',
          500.00, 1000.00, 500.00, 50.00],
         ['002', 'Maria Souza', 5, 'Mouse Gamer', 150.00, 400.00, 250.00, 62.50],
         ['003', 'Pedro Lima', 8, 'Monitor 24"', 1200.00, 2000.00, 800.00, 40.00],
         ['004', 'Ana Costa', 2, 'Notebook i7', 3500.00, 5000.00, 1500.00, 30.00],
         ['005', 'Carlos Mendes', 7, 'Headset', 300.00, 700.00, 400.00, 57.14],
         ['006', 'Fernanda Torres', 12, 'Cadeira Gamer', 800.00, 1500.00, 700.00, 46.67],
         ['007', 'Juliana Alves', 15, 'Impressora Multifuncional', 450.00, 1200.00, 750.00, 62.50],
         ['008', 'Roberto Dias', 20, 'Smartphone', 2000.00, 4500.00, 2500.00, 55.56],
         ['009', 'Letícia Nunes', 4, 'Tablet', 900.00, 1500.00, 600.00, 40.00],
         ['010', 'Rafael Rocha', 6, 'HD Externo 1TB', 400.00, 1000.00, 600.00, 60.00]]

# Configurar a tabela


dados_formatado = [cabecalho]

for data in datas:
    venda = Paragraph(f'00{data[0]}', custom_style)
    vendedor = Paragraph(data[1], custom_style)
    quantidade = Paragraph(locale.format_string('%.2f', data[2], grouping=True), custom_style)
    descricao = Paragraph(data[3], custom_style)
    custo = Paragraph(locale.format_string('%.2f', data[4], grouping=True), custom_style)
    faturamento = Paragraph(locale.format_string('%.2f', data[5], grouping=True), custom_style)
    lucro_rs = Paragraph(locale.format_string('%.2f', data[6], grouping=True), custom_style)
    lucro_p = Paragraph(f"{(data[6] / data[5]):.2%}".replace('.', ','), custom_style)

    dados_formatado.append([venda, vendedor, quantidade, descricao, custo, faturamento, lucro_rs, lucro_p])

table = Table(
    dados_formatado,
    colWidths=tamanho_colunas
)

table.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                           ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                           ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                           ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                           ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                           ('FONTSIZE', (0, 0), (-1, 0), 10),
                           ('FONTSIZE', (0, 1), (-1, -1), 7),
                           ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                           ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                           ('GRID', (0, 0), (-1, -1), 1, colors.black)]))

# Definir a posição da tabela
table.wrapOn(pdf, 20, 600)
table.drawOn(pdf, 20, 570)

# Inserir uma imagem no PDF
pdf.drawImage("../relatorio-A6.jpg", 50, 800, width=35, height=30)

# Finalizar o PDF
pdf.showPage()  # Para criar uma nova página, se necessário
pdf.save()  # Salva o arquivo PDF
