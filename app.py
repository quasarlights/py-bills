import os
import tkinter as tk
from tkinter import messagebox
from PyPDF2 import PdfFileReader, PdfFileWriter
import fitz  # Importa la biblioteca PyMuPDF
from PIL import ImageTk, Image
import time

class PDFViewerApp:
    def __init__(self, root):
        self.root = root
        self.pdf_folder = '/home/dit/Desktop/pdf'  # Ruta a la carpeta que contiene los archivos PDF
        self.pdf_files = []
        self.current_index = 0
        
        self.root.title("Visor de PDF")
        
        self.label = tk.Label(root, text="PDF Viewer", font=("Helvetica", 16))
        self.label.pack(pady=10)
        
        self.render_button = tk.Button(root, text="Renderizar", command=self.render_pdf)
        self.render_button.pack(pady=5)
        
        self.move1_button = tk.Button(root, text="Mover a Carpeta 1", command=self.move_to_folder1)
        self.move1_button.pack(pady=5)
        
        self.move2_button = tk.Button(root, text="Mover a Carpeta 2", command=self.move_to_folder2)
        self.move2_button.pack(pady=5)
        
        self.load_pdf_files()
    
    def load_pdf_files(self):
        self.pdf_files = [file for file in os.listdir(self.pdf_folder) if file.endswith(".pdf")]
        self.current_index = 0
        
    

    def render_pdf(self):
        if self.current_index < len(self.pdf_files):
            pdf_filename = self.pdf_files[self.current_index]
            pdf_path = os.path.join(self.pdf_folder, pdf_filename)

            try:
                doc = fitz.open(pdf_path)  # Abre el PDF utilizando PyMuPDF
                total_pages = doc.page_count  # Obtiene el número total de páginas del PDF

                # Crea una nueva ventana emergente para mostrar el contenido del PDF
                pdf_window = tk.Toplevel(self.root)
                pdf_window.title(pdf_filename)

                # Crea un lienzo de dibujo para mostrar las páginas del PDF
                canvas = tk.Canvas(pdf_window, width=600, height=800)
                canvas.pack()

                photo_list = []  # Lista para almacenar las referencias a los objetos PhotoImage

                for i in range(total_pages):
                    page = doc.load_page(i)
                    pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
                    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                    img = img.resize((int(img.width * 0.5), int(img.height * 0.5)))  # Ajusta el tamaño de la imagen
                    photo = ImageTk.PhotoImage(img)
                    photo_list.append(photo)  # Agrega el objeto PhotoImage a la lista
                    canvas.create_image(0, 0, image=photo, anchor=tk.NW)
                    pdf_window.update_idletasks()
                    time.sleep(0.1)  # Agrega un retraso para permitir que la ventana se actualice

                doc.close()  # Cierra el PDF después de mostrarlo

                self.photo_list = photo_list  # Almacena la lista de objetos PhotoImage como un atributo de la instancia

            except Exception as e:
                messagebox.showerror("Error", f"No se pudo abrir el archivo PDF:\n{str(e)}")
        else:
            messagebox.showinfo("Fin", "No hay más archivos PDF en la carpeta.")
    
    def move_to_folder1(self):
        self.move_to_folder("Carpeta1")
    
    def move_to_folder2(self):
        self.move_to_folder("Carpeta2")
    
    def move_to_folder(self, destination_folder):
        if self.current_index < len(self.pdf_files):
            pdf_filename = self.pdf_files[self.current_index]
            pdf_path = os.path.join(self.pdf_folder, pdf_filename)
            destination_path = os.path.join(destination_folder, pdf_filename)
            
            try:
                os.rename(pdf_path, destination_path)
                self.current_index += 1
                messagebox.showinfo("Mover PDF", f"Archivo PDF movido a {destination_folder}")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo mover el archivo PDF:\n{str(e)}")
        else:
            messagebox.showinfo("Fin", "No hay más archivos PDF en la carpeta.")
            
if __name__ == '__main__':
    root = tk.Tk()
    app = PDFViewerApp(root)
    root.mainloop()