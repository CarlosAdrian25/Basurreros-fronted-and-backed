from flask import Flask, render_template, Response
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Table, TableStyle
from reportlab.pdfgen import canvas
from io import BytesIO
from PIL import Image

app = Flask(__name__)

# Rutas de las imágenes
header_image_path = "alcaldia.jpg"  # Imagen de la izquierda
right_image_path = "pu.png"  # Imagen de la derecha

def adjust_opacity(image_path, opacity):
    """Ajusta la opacidad de una imagen y la guarda temporalmente."""
    img = Image.open(image_path).convert("RGBA")
    alpha = img.split()[3]  # Canal alfa
    alpha = alpha.point(lambda p: p * opacity)  # Ajustar opacidad
    img.putalpha(alpha)
    temp_path = "temp_image.png"
    img.save(temp_path)
    return temp_path

# Datos de ejemplo para la tabla
data = [
    ['ID', 'Nombre', 'Edad', 'Hora de Entrada', 'Hora de salida','Carro','Carro'],
    [1, 'Juan', 30, '12:30:15', '15:00:02','ESG56','ESG56'],
    [2, 'Ana', 25, '13:00:01', '16:00:13','ESG56','ESG56'],
    [3, 'Luis', 35, '13:00:08', '15:00:56','ESG56','ESG56'],
    [3, 'Luis', 35, '13:00:08', '15:00:56','ESG56','ESG56'],
    [3, 'Luis', 35, '13:00:08', '15:00:56','ESG56','ESG56'],
    [3, 'Luis', 35, '13:00:08', '15:00:56','ESG56','ESG56'],
    [3, 'Luis', 35, '13:00:08', '15:00:56','ESG56','ESG56'],
    [3, 'Luis', 35, '13:00:08', '15:00:56','ESG56','ESG56']
]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_pdf', methods=['GET'])
def generate_pdf():
    
    output = BytesIO()
    pdf_canvas = canvas.Canvas(output, pagesize=letter)
    page_width, page_height = letter

    
    left_margin = 25
    right_margin = 25
    top_margin = 15
    bottom_margin = 15
    content_width = page_width - left_margin - right_margin
   
    header_height = 70   
    image_width = 70  
    right_image_width = 70  
    text_start_x = left_margin + 75  
    text_start_y = page_height - top_margin - 35  

    
    try:
        pdf_canvas.drawImage(header_image_path, left_margin, page_height - top_margin - header_height - 20, width=image_width, height=header_height)
    except Exception as e:
        return f"Error al cargar la imagen del encabezado: {str(e)}"

   
    try:
        pdf_canvas.drawImage(right_image_path, page_width - right_margin - 15 - right_image_width, page_height - top_margin - header_height - 20, width=right_image_width, height=header_height)
    except Exception as e:
        return f"Error al cargar la imagen de la derecha: {str(e)}"

    
    pdf_canvas.setFont("Helvetica-Bold", 14)
    pdf_canvas.drawString(text_start_x, text_start_y, "GOBIERNO")
    pdf_canvas.drawString(text_start_x, text_start_y - 15, "AUTONOMO")
    pdf_canvas.drawString(text_start_x, text_start_y - 30, "MUNICIPAL")
    pdf_canvas.drawString(text_start_x, text_start_y - 45, "COLCAPIRHUA")
    pdf_canvas.setFont("Helvetica-Bold", 24)
    pdf_canvas.drawString(text_start_x + 80, text_start_y - 120, "REPORTE DE UNIDAD")
    pdf_canvas.setFont("Helvetica", 12)
    pdf_canvas.drawString(text_start_x + 150, text_start_y - 135, "(Informe Informativo)")

    
    line_start_x = left_margin + 100
    line_end_x = page_width - right_margin - 100
    line_y = text_start_y - 145  # Coordenada Y para la línea
    pdf_canvas.setLineWidth(1)  # Grosor de la línea
    pdf_canvas.line(line_start_x, line_y, line_end_x, line_y)

    
    background_image_path = "alcaldia.jpg"
    try:
        temp_image_path = adjust_opacity(background_image_path, 0.3)  # Opacidad al 30%
        background_width = 400
        background_height = 400
        background_x = (page_width - background_width) / 2
        background_y = (page_height - background_height) / 2
        pdf_canvas.drawImage(temp_image_path, background_x, background_y - 50, 
                            width=background_width, height=background_height, mask='auto')
    except Exception as e:
        return f"Error al cargar la imagen de fondo: {str(e)}"

     # Calcular ancho de columnas automáticamente
    num_columns = len(data[0])  # Número de columnas
    col_widths = [content_width / num_columns] * num_columns
    
    # Dibujar la tabla
    table = Table(data, colWidths=80, rowHeights=30)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), '#4caf50'),
        ('BACKGROUND', (0, 1), (-1, -1), 'white'), 
        ('TEXTCOLOR', (0, 0), (-1, 0), 'white'),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 1, 'black'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica')
    ]))

    
    table_width, table_height = table.wrap(0, 0)
    if table_width > content_width:
        table_width = - content_width
         # Calcular las coordenadas para centrar la tabla con los márgenes
        x = (page_width - left_margin - right_margin - table_width) / 2 + left_margin
        y = (page_height - top_margin - bottom_margin - table_height) / 2  # Ajustar para dejar espacio para el encabezado
       
    
    else:
        # Calcular las coordenadas para centrar la tabla con los márgenes
        x = (page_width - left_margin - right_margin - table_width) / 2 + left_margin
        y = (page_height - top_margin - bottom_margin - table_height) / 2  # Ajustar para dejar espacio para el encabezado

    # Dibujar la tabla debajo del encabezado
    table.drawOn(pdf_canvas, x, y)

    # Finalizar el PDF
    pdf_canvas.save()

    # Volver al principio del archivo
    output.seek(0)

    # Enviar el PDF al navegador como respuesta
    return Response(output, content_type='application/pdf')

if __name__ == '__main__':
    app.run(debug=True)