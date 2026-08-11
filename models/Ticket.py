from fpdf import FPDF

def crear_pdf_fpdf(id_venta, cliente, total):
    # Crear PDF con tamaño personalizado para ticket (Ancho: 80mm, Alto: 150mm)
    pdf = FPDF(format=(80, 150))
    pdf.add_page()
    pdf.set_font("Arial", size=10)
    
    # Contenido del ticket
    pdf.cell(60, 10, txt="RANCHO 3 CULTIVOS", ln=1, align='C')
    pdf.cell(60, 10, txt=f"Venta ID: {id_venta}", ln=1)
    pdf.cell(60, 10, txt=f"Cliente: {cliente}", ln=1)
    pdf.cell(60, 10, txt=f"Total: ${total}", ln=1)
    
    # Guardar archivo PDF
    nombre_archivo = f"ticket_{id_venta}.pdf"
    pdf.output(nombre_archivo)
    return nombre_archivo
