# Fix Error CWE-330
import secrets
from datetime import datetime

from PIL import Image

# PdfReader and PdfWriter are used for reading and writing PDF files
from pypdf import PdfReader as PdfFileReader
from pypdf import PdfWriter as PdfFileWriter

# Importing colors for setting table and text colors in the PDF
from reportlab.lib import colors

# Importing letter for setting the page size to letter format
from reportlab.lib.pagesizes import letter

# Importing getSampleStyleSheet to get default styles for text
from reportlab.lib.styles import getSampleStyleSheet

# Importing inch to use inch units for positioning elements in the PDF
from reportlab.lib.units import inch

# Importing stringWidth to calculate the width of text strings
from reportlab.pdfbase.pdfmetrics import stringWidth

# Importing canvas to create and manipulate PDF pages
from reportlab.pdfgen import canvas

# Importing Paragraph, Table, and TableStyle for creating and styling tables in the PDF
from reportlab.platypus import Paragraph, Table, TableStyle

# Importing necessary modules for PDF manipulation and creation


"""
# Issue: [B311:blacklist] Standard pseudo-random generators are not suitable for security/cryptographic purposes.
# Severity: Low   Confidence: High
# CWE: CWE-330 (https://cwe.mitre.org/data/definitions/330.html)

# vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

# import random
# num = random.randint(100, 900)
"""


num = secrets.randbelow(801) + 100  # Gera um número entre 100 e 900


def create_watermark_pdf(image_path: str, output_pdf: str):
    """
    Creates a PDF with a watermark image positioned at the top right corner.
    Args:
        image_path (str): The file path to the image to be used as a watermark.
        output_pdf (str): The file path where the output PDF will be saved.
    Returns:
        None
    """

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
    c.drawImage(image_path, x, y, width=new_width, height=new_height, mask="auto")
    c.save()


def add_watermark(input_pdf: str, output_pdf: str, watermark_pdf: str):
    """
    Adds a watermark to each page of the input PDF and saves the result to the output PDF.

    Args:
        input_pdf (str): The file path to the input PDF.
        output_pdf (str): The file path where the output PDF with watermark will be saved.
        watermark_pdf (str): The file path to the PDF containing the watermark.

    Returns:
        None
    """
    input_file = open(input_pdf, "rb")  # Open the input PDF file in read-binary mode
    watermark_file = open(
        watermark_pdf, "rb"
    )  # Open the watermark PDF file in read-binary mode

    input_pdf_reader = PdfFileReader(
        input_file
    )  # Create a PDF reader object for the input PDF
    watermark_pdf_reader = PdfFileReader(
        watermark_file
    )  # Create a PDF reader object for the watermark PDF

    output_pdf_writer = PdfFileWriter()  # Create a PDF writer object for the output PDF

    for page_num in range(len(input_pdf_reader.pages)):
        page = input_pdf_reader.pages[page_num]  # Get each page from the input PDF
        watermark_page = watermark_pdf_reader.pages[
            0
        ]  # Get the first page of the watermark PDF
        page.merge_page(watermark_page)  # Merge the watermark with the current page
        output_pdf_writer.add_page(page)  # Add the watermarked page to the output PDF

    with open(output_pdf, "wb") as output_file:
        output_pdf_writer.write(output_file)  # Write the output PDF to a file

    input_file.close()  # Close the input PDF file
    watermark_file.close()  # Close the watermark PDF file


def adjust_image_transparency(image_path: str, output_path: str, transparency):
    """
    Adjusts the transparency of an image and saves the result.

    Args:
        image_path (str): The file path to the input image.
        output_path (str): The file path where the output image will be saved.
        transparency (float): The transparency level to be applied (0.0 to 1.0).

    Returns:
        None
    """
    img = Image.open(image_path)  # Open the image file
    img = img.convert("RGBA")  # Convert the image to RGBA mode to handle transparency

    # Adjust the opacity
    data = img.getdata()  # Get image data
    new_data = []
    for item in data:
        # Modify the alpha value based on the transparency parameter
        new_data.append((item[0], item[1], item[2], int(item[3] * transparency)))
    img.putdata(new_data)  # Update image data with new transparency values

    # Save the adjusted image
    img.save(output_path, "PNG")  # Save the image in PNG format


def draw_table(c, x, y, data, max_width=5.5 * inch, min_font_size=4):
    """
    Draws a table on the given canvas at the specified position with the provided data.

    Args:
        c (canvas.Canvas): The canvas object where the table will be drawn.
        x (float): The x-coordinate of the table's position.
        y (float): The y-coordinate of the table's position.
        data (list): A list of lists containing the table data.
        max_width (float): The maximum width of the table (default is 5.5 inches).
        min_font_size (int): The minimum font size to be used (default is 4).

    Returns:
        None
    """
    styles = getSampleStyleSheet()
    style = styles["BodyText"]
    style.wordWrap = "Word"  # Enable word wrapping

    data2 = []  # List to hold the processed table data
    col_widths = [0] * len(data[0])  # List to hold the width of each column

    # Convert data and calculate required width/height
    for row in data:
        new_row = []
        for index, item in enumerate(row):
            p = Paragraph(str(item), style)  # Create a Paragraph object for each item
            new_row.append(p)
            text_width = (
                stringWidth(str(item), style.fontName, style.fontSize) + 10
            )  # Calculate text width with buffer
            if text_width > col_widths[index]:
                col_widths[index] = text_width  # Update column width if necessary
        data2.append(new_row)

    total_width = sum(col_widths)  # Calculate total width of the table
    if total_width > max_width:
        # Resize column widths proportionally if total width exceeds the maximum
        scale_factor = max_width / total_width
        col_widths = [width * scale_factor for width in col_widths]
        # Reduce font size if still too wide
        while total_width > max_width and style.fontSize > min_font_size:
            style.fontSize -= 1
            total_width = sum(
                stringWidth(str(item), style.fontName, style.fontSize) + 10
                for item in row
                for row in data2
            )

    table = Table(
        data2, colWidths=col_widths
    )  # Create the table with adjusted column widths
    table.setStyle(
        TableStyle(
            [
                (
                    "INNERGRID",
                    (0, 0),
                    (-1, -1),
                    0.25,
                    colors.black,
                ),  # Set inner grid lines
                ("BOX", (0, 0), (-1, -1), 0.25, colors.black),  # Set outer box lines
                ("FONTNAME", (0, 0), (-1, -1), style.fontName),  # Set font name
                ("FONTSIZE", (0, 0), (-1, -1), style.fontSize),  # Set font size
            ]
        )
    )

    table.wrapOn(c, x, y)  # Wrap the table on the canvas
    table.drawOn(c, x, y - table._height)  # Draw the table on the canvas


def create_EPI_control_sheet(
    filename: str, employee_data: dict[str, str], item_data: list[str], logo_path: str
):
    """
    Creates a PDF document for EPI (Personal Protective Equipment) control and delivery sheet.
    Args:
        filename (str): The name of the PDF file to be created.
        employee_data (dict[str, str]): A dictionary containing employee details such as company, name, registration, department, and position.
        item_data (list[str]): A list of strings representing the items to be included in the document.
        logo_path (str): The file path to the company logo image.
    Returns:
        None
    """
    c = canvas.Canvas(filename, pagesize=letter)
    logo_width = 75  # Largura em pontos

    # Obter as dimensões originais da imagem para calcular a altura proporcional
    img = Image.open(logo_path)
    original_width, original_height = img.size
    logo_height = original_height * (
        logo_width / original_width
    )  # Mantendo a proporção

    # Ajustar a posição vertical para que a logo não ultrapasse o limite superior da página
    logo_y_position = 10.5 * inch - logo_height
    if logo_y_position < 0:
        # Evita que a logo ultrapasse a margem superior da página
        logo_y_position = 0.5 * inch

    # Ajustar a posição do texto para não sobrepor a logo
    c.setFont("Helvetica-Bold", 12)
    text_position_y = logo_y_position + logo_height + 0.1 * inch
    c.drawString(0.5 * inch, text_position_y, "FICHA DE CONTROLE E ENTREGA")
    c.line(
        x1=0.5 * inch,
        y1=text_position_y - 0.1 * inch,
        x2=5.5 * inch,
        y2=text_position_y - 0.1 * inch,
    )  # Linha divisória

    c.setFont("Helvetica", 10)
    c.drawString(0.5 * inch, 10 * inch, f"Empresa: {employee_data['company']}")
    c.drawString(0.5 * inch, 9.8 * inch, f"Funcionário: {employee_data['name']}")
    c.drawString(0.5 * inch, 9.6 * inch, f"Registro: {employee_data['registration']}")
    c.drawString(
        0.5 * inch, 9.4 * inch, f"Departamento: {employee_data['departamento']}"
    )
    c.drawString(4.5 * inch, 9.4 * inch, f"Cargo: {employee_data['cargo']}")

    # ... Adicione outros detalhes do funcionário

    # Desenha a seção "Entrega"
    c.drawString(0.5 * inch, 8.6 * inch, f"ENTREGA {employee_data['lancamento_code']}")
    c.drawString(
        3.7 * inch,
        8.6 * inch,
        f'Data da Entrega: {datetime.now().strftime("%d/%m/%Y")}',
    )
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
    c.drawString(0.5 * inch, 1.5 * inch, "____________________________________________")
    c.drawString(0.5 * inch, 1.3 * inch, "Assinatura do Funcionário")

    c.drawString(4.5 * inch, 1.5 * inch, "____________________________________________")
    c.drawString(4.5 * inch, 1.3 * inch, "Assinatura do Entregador")

    # Finaliza o PDF
    c.showPage()
    c.save()
