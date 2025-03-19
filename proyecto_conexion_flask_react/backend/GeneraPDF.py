from fpdf import FPDF
import os

def GeneraPDF(contenido, nombre_pdf="informe_generado.pdf"):

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    public_dir = os.path.join(base_dir, "public")
    ruta_pdf = os.path.join(public_dir, nombre_pdf)

    if os.path.exists(ruta_pdf):
        os.remove(ruta_pdf)  # Eliminar archivo existente
    txt_path = guardar_string_como_txt(contenido, "archivo")

    # Ruta absoluta hacia ../public
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Esto te deja en la raíz del proyecto
    public_dir = os.path.join(base_dir, "public")
    os.makedirs(public_dir, exist_ok=True)

    output_pdf_path = os.path.join(public_dir, nombre_pdf)

    exportar_txt_a_pdf(txt_path, output_pdf_path)
    return output_pdf_path  # Puedes devolverlo para usarlo en la API

def guardar_string_como_txt(contenido, nombre_archivo):
    ruta = os.path.abspath(f"{nombre_archivo}.txt")
    with open(ruta, "w", encoding="utf-8") as archivo:
        archivo.write(contenido)
    print(f"Archivo '{ruta}' guardado correctamente.")
    return ruta

def exportar_txt_a_pdf(txt_path, output_pdf_path):
    try:
        with open(txt_path, 'r', encoding='utf-8') as file:
            contenido = file.readlines()

        pdf = FPDF()
        pdf.add_page()

        font_path = os.path.join(os.getcwd(), "DejaVuSans.ttf")
        pdf.add_font("DejaVu", "", font_path, uni=True)
        pdf.set_font("DejaVu", size=12)

        for linea in contenido:
            pdf.multi_cell(0, 10, linea.strip())

        pdf.output(output_pdf_path)
        print(f"PDF generado en: {output_pdf_path}")

    except Exception as e:
        print(f"Error generando PDF: {e}")
