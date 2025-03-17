from fpdf import FPDF
from tkinter import Tk, filedialog, messagebox
import os


def GeneraPDF(contenido):
    exportar_txt_a_pdf(guardar_string_como_txt(contenido, "archivo"))


def leer_txt_como_string(ruta_archivo):
    with open(ruta_archivo, "r", encoding="utf-8") as archivo:
        contenido = archivo.read()
    return contenido

def guardar_string_como_txt(contenido, nombre_archivo):
    ruta = os.path.abspath(f"{nombre_archivo}.txt")
    with open(ruta, "w", encoding="utf-8") as archivo:
        archivo.write(contenido)
    print(f"Archivo '{ruta}' guardado correctamente.")
    return ruta


def exportar_txt_a_pdf(txt_path):
    # Ocultamos la ventana principal de tkinter
    root = Tk()
    root.withdraw()

    # Abrimos el diálogo "Guardar como" solo para PDF
    ruta_pdf = filedialog.asksaveasfilename(
        defaultextension=".pdf",
        filetypes=[("PDF files", "*.pdf")],
        title="Guardar PDF como"
    )

    if ruta_pdf:
        try:
            # Leer el archivo txt
            with open(txt_path, 'r', encoding='utf-8') as file:
                contenido = file.readlines()

            # Crear el PDF
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            for linea in contenido:
                pdf.multi_cell(0, 10, linea.strip())

            pdf.output(ruta_pdf)
            messagebox.showinfo("Éxito", f"PDF guardado en:\n{ruta_pdf}")

        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error: {e}")
    else:
        messagebox.showinfo("Cancelado", "No se seleccionó ninguna ubicación.")
