import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import pyodbc

class CursoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Curso Aplicación E.E.T N°21")

        self.root.resizable(True, True)
        self.root.configure(bg="MediumSeaGreen")

        self.conn = None
        self.tree = None

        self.create_widgets()
        self.connect_to_db()
        self.load_data()

    def adjust_window_size(self):
        num_rows = len(self.tree.get_children())
        total_height = 20 + num_rows * 24
        min_height = 400
        new_height = max(min_height, total_height)
        self.root.geometry(f"1200x{new_height}")
        self.adjust_window_size()

    def create_widgets(self):
        frame_izquierda = tk.Frame(self.root, width=400, height=400, bg="MediumSeaGreen")
        frame_izquierda.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        frame_derecha = tk.Frame(self.root, width=700, height=600, bg="MediumSeaGreen")
        frame_derecha.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        self.create_data_entry_widgets(frame_izquierda)
        self.create_treeview_widget(frame_derecha)
        self.create_buttons(frame_izquierda)
        self.tree.bind("<<TreeviewSelect>>", self.load_data_to_entries)

    def create_data_entry_widgets(self, frame):
        labels = ["id_curso", "annio", "division", "id_materia"]
        self.entry_vars = {}
        for i, label_text in enumerate(labels):
            label = tk.Label(frame, text=label_text + ": ", bg="MediumSeaGreen")
            label.grid(row=i, column=0, sticky="e")

            entry_var = tk.StringVar()
            entry = tk.Entry(frame, textvariable=entry_var)
            entry.grid(row=i, column=1, padx=10, pady=5)
            self.entry_vars[label_text] = entry_var

    def create_treeview_widget(self, frame):
        self.tree = ttk.Treeview(frame, columns=("id_curso", "annio", "division", "id_materia"))
        self.tree.heading("#1", text="ID Curso")
        self.tree.heading("#2", text="Año")
        self.tree.heading("#3", text="División")
        self.tree.heading("#4", text="ID Materia")
        self.tree.grid()
        self.tree.column("#0", width=0)
        self.tree.column("#1", width=150)
        self.tree.column("#2", width=150)
        self.tree.column("#3", width=150)
        self.tree.column("#4", width=150)

    def create_buttons(self, frame):
        agregar_button = tk.Button(frame, text="Agregar Registro", command=self.agregar, height=2, width=15)
        agregar_button.grid(row=10, column=1, pady=10)

        borrar_button = tk.Button(frame, text="Borrar", command=self.borrar_registro)
        borrar_button.grid(row=10, column=0)

        modificar_button = tk.Button(frame, text="Modificar", command=self.modificar_registro)
        modificar_button.grid(row=10, column=2, padx=10)

        boton_conectar = tk.Button(frame, text="SQL Server", command=self.connect_to_db)
        boton_conectar.grid(row=11, column=0, padx=10)

        consultar_button = tk.Button(frame, text="Consultar", command=self.consultar_datos)
        consultar_button.grid(row=11, column=1, padx=10)

        salir_button = tk.Button(frame, text="Salir", command=self.salir, bg="red", fg="white", width=10)
        salir_button.grid(row=11, column=2, pady=10)

    def connect_to_db(self):
        try:
            self.conn = pyodbc.connect('Driver={SQL Server};'
                                       'Server=Tssit01;'
                                       'Database=rodrigo1;'
                                       'UID=Soporte;'
                                       'PWD=Instituto_2023')
            messagebox.showinfo("Conexión Exitosa", "Conexión a la base de datos exitosa.")
        except Exception as e:
            messagebox.showerror("Error de Conexión", f"Error al conectar a la base de datos:\n{str(e)}")

    def agregar(self):
        datos = {label: var.get() for label, var in self.entry_vars.items()}

        try:
            cursor = self.conn.cursor()
            cursor.execute("INSERT INTO curso (annio, division, id_materia) "
                           "VALUES (?, ?, ?)",
                           (datos["annio"], datos["division"], datos["id_materia"]))
            self.conn.commit()
            messagebox.showinfo("Registro Agregado", "El registro se ha agregado correctamente.")
            self.load_data()
            self.clear_entries()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo agregar el registro:\n{str(e)}")

    def borrar_registro(self):
        id_curso_a_borrar = self.entry_vars["id_curso"].get()

        if not id_curso_a_borrar:
            messagebox.showerror("Error", "Ingrese un ID de curso para borrar un registro.")
            return

        try:
            cursor = self.conn.cursor()
            cursor.execute("DELETE FROM curso WHERE id_curso=?", (id_curso_a_borrar,))
            self.conn.commit()
            messagebox.showinfo("Registro Borrado", "El registro se ha borrado correctamente.")
            self.load_data()
            self.clear_entries()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo borrar el registro:\n{str(e)}")

    def load_data_to_entries(self, event):
        selected_item = self.tree.selection()
        if selected_item:
            values = self.tree.item(selected_item, 'values')
            keys_order = ["id_curso", "annio", "division", "id_materia"]

            for i, key in enumerate(keys_order):
                if i < len(values):
                    var = self.entry_vars[key]
                    var.set(values[i])
                else:
                    var = self.entry_vars[key]
                    var.set("")

    def modificar_registro(self):
        datos = {label: var.get() for label, var in self.entry_vars.items()}
        id_curso_a_modificar = datos["id_curso"]

        if not id_curso_a_modificar:
            messagebox.showerror("Error", "Ingrese un ID de curso para modificar un registro.")
            return

        try:
            cursor = self.conn.cursor()
            cursor.execute("UPDATE curso SET annio=?, division=?, id_materia=? WHERE id_curso=?",
                           (datos["annio"], datos["division"], datos["id_materia"], id_curso_a_modificar))
            self.conn.commit()
            messagebox.showinfo("Registro Modificado", "El registro se ha modificado correctamente.")
            self.load_data()
            self.clear_entries()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo modificar el registro:\n{str(e)}")


    def consultar_datos(self):
        
        id_curso_consulta = self.entry_vars["id_curso"].get()

        if not id_curso_consulta:
            messagebox.showerror("Error", "Ingrese un ID de curso para buscar un registro.")
            return

        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM curso WHERE id_curso=?", (id_curso_consulta,))
            result = cursor.fetchone()

            if result is not None:
                messagebox.showinfo("Registro encontrado", "El registro se ha encontrado correctamente.")
                self.tree.delete(*self.tree.get_children())  # Limpiar la Treeview
                self.tree.insert("", "end", values=(result[0], result[1], result[2], result[3]))

            else:
                messagebox.showinfo("No se encontraron resultados", "No se encontraron registros con el ID de curso especificado.")

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo consultar el registro:\n{str(e)}")

    def load_data(self):
        if self.conn is not None:
            cursor = self.conn.cursor()
            cursor.execute('SELECT id_curso, annio, division, id_materia FROM curso')
            data = cursor.fetchall()
            self.clear_treeview()
            for row in data:
                self.tree.insert('', 'end', values=(row[0], row[1], row[2], row[3]))

    def clear_entries(self):
        for var in self.entry_vars.values():
            var.set("")

    def clear_treeview(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

    def salir(self):
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = CursoApp(root)
    root.mainloop()

    
