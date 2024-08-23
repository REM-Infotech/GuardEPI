from PyPDF2 import PdfWriter as PdfFileWriter
from PyPDF2 import PdfReader as PdfFileReader
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfbase.pdfmetrics import stringWidth
import os
from PIL import Image
import random
from datetime import datetime
num = random.randint(100, 900)


def create_watermark_pdf(image_path: str, output_pdf: str):
    
    c = canvas.Canvas(output_pdf, pagesize=letter)
    # Dimensões da página (em pontos, 1 ponto = 1/72 polegadas)
    width, height = letter

    # Carregando a imagem para obter suas dimensões originais
    img = Image.open(image_path)
    orig_width, orig_height = img.size

    # Calculando o novo tamanho da imagem (25% do original)
    new_width = orig_width * 0.25
    new_height = orig_height * 0.25

    # Posicionando a imagem no canto superior direito da página
    x = width - new_width  # X é calculado para colocar a imagem alinhada à direita
    y = height - new_height  # Y é calculado para colocar a imagem no topo da página

    # Desenhando a imagem
    c.drawImage(image_path, x, y, width=new_width,
                height=new_height, mask='auto')
    c.save()


def add_watermark(input_pdf: str, output_pdf: str, watermark_pdf: str):
    
    input_file = open(input_pdf, 'rb')
    watermark_file = open(watermark_pdf, 'rb')

    input_pdf_reader = PdfFileReader(input_file)
    watermark_pdf_reader = PdfFileReader(watermark_file)

    output_pdf_writer = PdfFileWriter()

    for page_num in range(len(input_pdf_reader.pages)):
        page = input_pdf_reader.pages[page_num]
        watermark_page = watermark_pdf_reader.pages[0]
        page.merge_page(watermark_page)
        output_pdf_writer.add_page(page)

    with open(output_pdf, 'wb') as output_file:
        output_pdf_writer.write(output_file)

    input_file.close()
    watermark_file.close()


def adjust_image_transparency(image_path: str, output_path: str, transparency):

    img = Image.open(image_path)
    img = img.convert("RGBA")

    # Ajusta a opacidade
    data = img.getdata()
    new_data = []
    for item in data:
        # Altera o valor alpha com base no parâmetro de transparência
        new_data.append((item[0], item[1], item[2],
                        int(item[3] * transparency)))
    img.putdata(new_data)

    # Salva a imagem ajustada
    img.save(output_path, "PNG")


def draw_table(c, x, y, data, max_width=5.5*inch, min_font_size=4):
    styles = getSampleStyleSheet()
    style = styles["BodyText"]
    style.wordWrap = 'Word'  # Habilita quebra de texto
    normal_font_size = style.fontSize

    # Converter dados e calcular largura/altura necessária
    data2 = []
    col_widths = [0] * len(data[0])
    for row in data:
        new_row = []
        for index, item in enumerate(row):
            p = Paragraph(item, style)
            new_row.append(p)
            text_width = stringWidth(
                item, style.fontName, style.fontSize) + 10  # Adiciona um buffer
            if text_width > col_widths[index]:
                col_widths[index] = text_width
        data2.append(new_row)

    total_width = sum(col_widths)
    if total_width > max_width:
        # Redimensiona as larguras das colunas proporcionalmente se a largura total exceder o máximo
        scale_factor = max_width / total_width
        col_widths = [width * scale_factor for width in col_widths]
        # Reduz o tamanho da fonte se ainda for muito largo
        while total_width > max_width and style.fontSize > min_font_size:
            style.fontSize -= 1
            total_width = sum(stringWidth(
                item, style.fontName, style.fontSize) + 10 for item in row for row in data2)

    table = Table(data2, colWidths=col_widths)
    table.setStyle(TableStyle([
        ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
        ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
        ('FONTNAME', (0, 0), (-1, -1), style.fontName),
        ('FONTSIZE', (0, 0), (-1, -1), style.fontSize),
    ]))

    table.wrapOn(c, x, y)
    table.drawOn(c, x, y - table._height)


def create_EPI_control_sheet(filename, employee_data, delivery_data, item_data, logo_path):
    c = canvas.Canvas(filename, pagesize=letter)
    logo_width = 75  # Largura em pontos

    # Obter as dimensões originais da imagem para calcular a altura proporcional
    img = Image.open(logo_path)
    original_width, original_height = img.size
    logo_height = original_height * \
        (logo_width / original_width)  # Mantendo a proporção

    # Ajustar a posição vertical para que a logo não ultrapasse o limite superior da página
    logo_y_position = 10.5 * inch - logo_height
    if logo_y_position < 0:
        # Evita que a logo ultrapasse a margem superior da página
        logo_y_position = 0.5 * inch

    # Ajustar a posição do texto para não sobrepor a logo
    c.setFont("Helvetica-Bold", 12)
    text_position_y = logo_y_position + logo_height + 0.1 * inch
    c.drawString(0.5 * inch, text_position_y, "FICHA DE CONTROLE E ENTREGA")
    c.line(x1=0.5 * inch, y1=text_position_y - 0.1 * inch, x2=5.5 *
           inch, y2=text_position_y - 0.1 * inch)  # Linha divisória

    c.setFont("Helvetica", 10)
    c.drawString(0.5 * inch, 10 * inch, f"Empresa: {employee_data['company']}")
    c.drawString(0.5 * inch, 9.8 * inch, f"Funcionário: {employee_data['name']}")
    c.drawString(0.5 * inch, 9.6 * inch, f"Registro: {employee_data['registration']}")
    c.drawString(0.5 * inch, 9.4 * inch, f"Departamento: {employee_data['departamento']}")
    c.drawString(4.5 * inch, 9.4 * inch, f"Cargo: {employee_data['cargo']}")

    # ... Adicione outros detalhes do funcionário

    # Desenha a seção "Entrega"
    c.drawString(0.5 * inch, 8.6 * inch, f"ENTREGA {employee_data['lancamento_code']}")
    c.drawString(3.7 * inch, 8.6 * inch,
                 F'Data da Entrega: {datetime.now().strftime("%d/%m/%Y")}')
    # Desenha o texto padrão
    standard_text_lines = [
        "Declaro para os devidos fins, que recebi os E.P.I's descritos e me comprometo:",
        "",
        "- Usá-los apenas para a finalidade que se destinam;",
        "- Responsabilizar-me pela sua guarda e conservação;",
        "- Comunicar ao empregador qualquer modificação que tornem impróprios para o uso;",
        "- Responsabilizar-me pela danificação do E.P.I. devivo ao uso inadequado ou fora das atividades ",
        "a que se destina, bem como pelo seu extravio;",
        "- Comprometendo-me a devolução em caso de desligamento da empresa no prazo de 24 horas após comunicação;",
        "",
        "Declaro ainda estar ciente que o uso é obrigatório. Sujeito a aplicação de penalidades",
        "conforme art. 158 Lei n°6.514, de 22/12/1977",
        "",
        "Declaro ainda ter recebido instruções e treinamento referente ao uso correto de E.P.I. e as Normas de Segurança do Trabalho.",
        # ... Adicione outras linhas de texto padrão
    ]
    current_height = 8.2 * inch
    line_height = 0.2 * inch
    for line in standard_text_lines:
        c.drawString(0.5 * inch, current_height, line)
        current_height -= line_height

    # Define a altura da tabela
    table_height = current_height - 0.3 * inch

    # Desenha a tabela
    draw_table(c, 0.5 * inch, table_height, item_data)

    # Desenha as assinaturas
    c.drawString(0.5 * inch, 1.5 * inch,
                 "____________________________________________")
    c.drawString(0.5 * inch, 1.3 * inch, "Assinatura do Funcionário")

    # c.drawString(4.5 * inch, 1.5 * inch, "____________________________________________")
    # c.drawString(4.5 * inch, 1.3 * inch, "Assinatura do Responsável")

    # Finaliza o PDF
    c.showPage()
    c.save()
