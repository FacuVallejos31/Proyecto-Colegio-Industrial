import tkinter as tk
from tkinter import ttk
import subprocess

class MenuPrincipalApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Menu Aplicaciones")
        self.root.geometry("650x650")  # Ajusta el tamaño de la ventana principal
        self.root.configure(bg="SeaGreen")

        # Configuración de estilo
        self.style = ttk.Style()
        self.style.configure('TButton', font=('Helvetica', 16), padding=5)

        # Agregar título
        titulo_label = tk.Label(self.root, text="Menu Aplicaciones", font=('Helvetica', 16, 'bold'))
        titulo_label.pack(pady=10)

        # Crear botones
        opciones = ["Alumno", "Asistencia", "Personal", "Curso", "Especialidad", "Materia", "Nota", "Agenda"]
        funciones = [self.abrir_aplicacion] * 8

        for opcion, app_function in zip(opciones, funciones):
            btn = ttk.Button(self.root, text=opcion, command=app_function)
            btn.pack(fill=tk.X, padx=30, pady=10)

        # Botón Acerca de
        acerca_de_btn = ttk.Button(self.root, text="Acerca de", command=self.abrir_archivo_txt)
        acerca_de_btn.pack(fill=tk.X, padx=30, pady=10)

    def abrir_aplicacion(self):
        # Agrega aquí la lógica para abrir la aplicación correspondiente
        pass

    def abrir_archivo_txt(self):
        # Especifica la ruta de tu archivo .txt
        archivo_txt = "C:/Users/facuv/OneDrive/Documentos/Programas python/Final/Informacion.txt"
        try:
            subprocess.run(["notepad.exe", archivo_txt], check=True)
        except subprocess.CalledProcessError:
            print(f"No se pudo abrir {archivo_txt} con Notepad.")

if __name__ == "__main__":
    root = tk.Tk()
    app = MenuPrincipalApp(root)
    root.mainloop()
