from pathlib import Path

from fpdf import FPDF

def crear_pdf_fpdf(
    id_venta,
    cliente,
    total,
    fecha="",
    producto="",
    cantidad=0,
):
    """Genera un ticket PDF con diseño crema y devuelve su ruta."""
    carpeta_tickets = Path("tickets")
    carpeta_tickets.mkdir(exist_ok=True)
    ruta_archivo = carpeta_tickets / f"ticket_{id_venta}.pdf"

    # Paleta visual del sistema Rancho Tres Cultivos.
    CREMA = (250, 244, 234)
    CREMA_OSCURO = (229, 214, 197)
    CAFE = (94, 70, 45)
    DORADO = (168, 129, 86)
    BLANCO = (255, 255, 255)
    TEXTO = (48, 43, 38)
    GRIS = (105, 98, 90)

    # Ticket compacto de 80 mm de ancho por 180 mm de alto.
    pdf = FPDF(format=(80, 180))
    pdf.set_margins(5, 5, 5)
    pdf.set_auto_page_break(auto=True, margin=5)
    pdf.add_page()

    # Fondo crema completo.
    pdf.set_fill_color(*CREMA)
    pdf.rect(0, 0, 80, 180, style="F")

    # Encabezado café con bordes suaves visuales.
    pdf.set_fill_color(*CAFE)
    pdf.rect(4, 4, 72, 43, style="F")

    # Logo centrado; la ruta funciona aunque app.py se ejecute desde otra carpeta.
    ruta_proyecto = Path(__file__).resolve().parent.parent
    ruta_logo = ruta_proyecto / "assets" / "logo_rancho.png"
    if ruta_logo.exists():
        pdf.image(str(ruta_logo), x=29, y=7, w=22, h=22, keep_aspect_ratio=True)

    pdf.set_xy(5, 30)
    pdf.set_text_color(*BLANCO)
    pdf.set_font("Helvetica", style="B", size=13)
    pdf.cell(70, 6, text="RANCHO 3 CULTIVOS", new_x="LMARGIN", new_y="NEXT", align="C")
    pdf.set_font("Helvetica", size=7)
    pdf.cell(70, 5, text="COMPROBANTE DE VENTA", new_x="LMARGIN", new_y="NEXT", align="C")
    pdf.set_text_color(235, 220, 201)
    pdf.cell(70, 4, text="Calidad y confianza en cada compra", align="C")

    # Bloque de información general.
    pdf.set_xy(5, 51)
    pdf.set_fill_color(*CREMA_OSCURO)
    pdf.set_text_color(*CAFE)
    pdf.set_font("Helvetica", style="B", size=9)
    pdf.cell(70, 7, text="DATOS DE LA VENTA", new_x="LMARGIN", new_y="NEXT", align="C", fill=True)

    pdf.set_fill_color(*BLANCO)
    pdf.set_draw_color(*DORADO)
    pdf.set_text_color(*TEXTO)
    pdf.set_font("Helvetica", style="B", size=8)
    pdf.cell(22, 6, text="  Folio", border="L", fill=True)
    pdf.set_font("Helvetica", size=8)
    pdf.cell(48, 6, text=f"VENTA-{int(id_venta):06d}", border="R", new_x="LMARGIN", new_y="NEXT", fill=True)
    if fecha:
        pdf.set_font("Helvetica", style="B", size=8)
        pdf.cell(22, 6, text="  Fecha", border="L", fill=True)
        pdf.set_font("Helvetica", size=8)
        pdf.cell(48, 6, text=str(fecha), border="R", new_x="LMARGIN", new_y="NEXT", fill=True)
    pdf.set_font("Helvetica", style="B", size=8)
    pdf.cell(22, 7, text="  Cliente", border="LB", fill=True)
    pdf.set_font("Helvetica", size=8)
    pdf.cell(48, 7, text=str(cliente)[:38], border="RB", new_x="LMARGIN", new_y="NEXT", fill=True)

    # Detalle de compra con una estructura tipo tabla.
    pdf.ln(4)
    pdf.set_fill_color(*CREMA_OSCURO)
    pdf.set_text_color(*CAFE)
    pdf.set_font("Helvetica", style="B", size=9)
    pdf.cell(70, 7, text="DETALLE DE COMPRA", new_x="LMARGIN", new_y="NEXT", align="C", fill=True)

    pdf.set_fill_color(*CAFE)
    pdf.set_text_color(*BLANCO)
    pdf.set_font("Helvetica", style="B", size=8)
    pdf.cell(48, 7, text="Producto / cultivo", border=1, align="C", fill=True)
    pdf.cell(22, 7, text="Cantidad", border=1, new_x="LMARGIN", new_y="NEXT", align="C", fill=True)

    pdf.set_fill_color(*BLANCO)
    pdf.set_text_color(*TEXTO)
    pdf.set_font("Helvetica", size=8)
    pdf.cell(48, 10, text=str(producto or "Sin especificar")[:31], border=1, align="C", fill=True)
    pdf.cell(22, 10, text=str(cantidad), border=1, new_x="LMARGIN", new_y="NEXT", align="C", fill=True)

    # Total destacado en una caja café.
    pdf.ln(5)
    pdf.set_fill_color(*CAFE)
    pdf.set_text_color(*BLANCO)
    pdf.set_font("Helvetica", style="B", size=13)
    pdf.cell(70, 12, text=f"TOTAL  $ {float(total):,.2f}", new_x="LMARGIN", new_y="NEXT", align="C", fill=True)

    # Pie lógico del comprobante.
    pdf.ln(5)
    pdf.set_text_color(*CAFE)
    pdf.set_font("Helvetica", style="B", size=10)
    pdf.cell(70, 6, text="GRACIAS POR SU COMPRA", new_x="LMARGIN", new_y="NEXT", align="C")
    pdf.set_text_color(*GRIS)
    pdf.set_font("Helvetica", size=7)
    pdf.cell(70, 5, text="Conserve este comprobante para cualquier aclaracion.", new_x="LMARGIN", new_y="NEXT", align="C")
    pdf.cell(70, 5, text="Documento generado por el sistema de ventas.", new_x="LMARGIN", new_y="NEXT", align="C")

    pdf.ln(2)
    pdf.set_draw_color(*DORADO)
    pdf.set_line_width(0.4)
    pdf.line(14, pdf.get_y(), 66, pdf.get_y())
    pdf.ln(3)
    pdf.set_text_color(*DORADO)
    pdf.set_font("Helvetica", style="I", size=7)
    pdf.cell(70, 4, text=f"Ticket #{id_venta}", align="C")

    pdf.output(str(ruta_archivo))
    return str(ruta_archivo.resolve())