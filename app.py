from flask import Flask, render_template, request, send_file
import os
from datetime import datetime
from PyPDF2 import PdfMerger
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

app = Flask(__name__)

DATA_FOLDER = "data"
OUTPUT_FOLDER = "outputs"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route("/")
def index():
    # listar PDFs como opciones
    pdfs = [f for f in os.listdir(DATA_FOLDER) if f.endswith(".pdf")]
    return render_template("index.html", pdfs=pdfs)

@app.route("/generar", methods=["POST"])
def generar():
    cliente = request.form["cliente"]
    producto_pdf = request.form["producto"]

    # generar PDF temporal con datos de cotización
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    cotizacion_pdf = os.path.join(OUTPUT_FOLDER, f"cotizacion_{timestamp}.pdf")

    styles = getSampleStyleSheet()
    doc = SimpleDocTemplate(cotizacion_pdf)
    story = [
        Paragraph("Cotización", styles["Title"]),
        Spacer(1, 20),
        Paragraph(f"Cliente: {cliente}", styles["Normal"]),
        Paragraph(f"Producto seleccionado: {producto_pdf}", styles["Normal"]),
        Spacer(1, 20),
        Paragraph("Gracias por su preferencia.", styles["Italic"]),
    ]
    doc.build(story)

    # fusionar con el PDF de base
    final_pdf = os.path.join(OUTPUT_FOLDER, f"cotizacion_final_{timestamp}.pdf")
    merger = PdfMerger()
    merger.append(cotizacion_pdf)
    merger.append(os.path.join(DATA_FOLDER, producto_pdf))
    merger.write(final_pdf)
    merger.close()

    return send_file(final_pdf, as_attachment=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
