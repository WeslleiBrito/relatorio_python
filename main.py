from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle
from datetime import date


class RelatorioItem:
    def __init__(self):
        self.__pdf = canvas.Canvas(f"LUCRATIVIDADE-{date.today()}.pdf", pagesize=A4)
        self.__tamanho_colunas = [50, 50, 170, 60, 40, 40, 50, 50, 50]

        # Definir margens e espaçamentos
        self.top_margin_first_page = 700  # Espaço reservado para o cabeçalho na primeira página
        self.top_margin_other_pages = 750  # Pequeno espaço nas páginas subsequentes
        self.left_margin = 20
        self.bottom_margin = 50  # Margem inferior da tabela

    def gerar_cabecalho_primeira_pagina(self):
        # Cabeçalho com informações no topo da primeira página
        self.__pdf.drawString(100, 800, "Relatório de Lucratividade")
        self.__pdf.drawString(100, 780, f"Data: {date.today()}")
        self.__pdf.drawString(100, 760, "Período: 01/01/2024 a 31/12/2024")

    def gerar_tabela(self):
        # Simulação de dados de tabela
        dados = [[str(i), f"Produto {i}", f"{i * 10}", f"{i * 20}", f"{i * 30}", f"{i * 40}"] for i in range(50)]
        tabela = Table(dados, colWidths=self.__tamanho_colunas)

        # Estilizar a tabela
        estilo_tabela = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ])
        tabela.setStyle(estilo_tabela)

        # Calcular a altura da tabela
        available_width, available_height = A4

        # Desenhar na primeira página com cabeçalho
        pos_y = self.top_margin_first_page  # Começa a tabela mais abaixo na primeira página
        self.gerar_cabecalho_primeira_pagina()  # Inserir o cabeçalho na primeira página

        # Verificar se a tabela cabe na página
        required_width, required_height = tabela.wrap(available_width, available_height)

        # Variável para rastrear a tabela restante
        remaining_table = tabela

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


if __name__ == '__main__':
    relatorio = RelatorioItem()
    relatorio.gerar_tabela()
