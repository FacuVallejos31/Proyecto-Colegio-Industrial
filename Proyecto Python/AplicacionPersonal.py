# Importar las bibliotecas necesarias
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import pyodbc

class PersonalApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Agenda Personal E.E.T N°21")
        #self.root.geometry("1300x600")
        self.root.resizable(True, True)
        self.root.configure(bg="MediumSeaGreen")
        #self.root.iconbitmap("logo.ico")
        self.root.grid_propagate(True)
        
        self.conn = None
        self.tree = None
        
        self.create_widgets()
        self.connect_to_db()
        self.load_data()

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
        labels = ["ID Personal","DNI", "Nombre", "Apellido", "Legajo", "Direccion", "Telefono", "Rol", "Fecha Nacimiento"]
        self.entry_vars = {}
        for i, label_text in enumerate(labels):
            label = tk.Label(frame, text=label_text + ": ", bg="MediumSeaGreen", fg="Black")
            label.grid(row=i, column=0, sticky="e")
        
            entry_var = tk.StringVar()
            entry = tk.Entry(frame, textvariable=entry_var)
            entry.grid(row=i, column=1, padx=10, pady=5)
            self.entry_vars[label_text] = entry_var
     
    def create_treeview_widget(self, frame):
        self.tree = ttk.Treeview(frame, columns=("ID Personal", "dni_personal", "nombre_personal", "apellido_personal", "legajo", "direccion", "telefono", "rol", "fecha_nacimiento"))
        self.tree.heading("#1", text="ID Personal")
        self.tree.heading("#2", text="DNI")
        self.tree.heading("#3", text="Nombre")
        self.tree.heading("#4", text="Apellido")
        self.tree.heading("#5", text="Legajo")
        self.tree.heading("#6", text="Direccion")
        self.tree.heading("#7", text="Telefono")
        self.tree.heading("#8", text="Rol")
        self.tree.heading("#9", text="Fecha Nacimiento")
        self.tree.grid()
        self.tree.column("#0", width=10)
        self.tree.column("#1", width=90)
        self.tree.column("#2", width=90)
        self.tree.column("#3", width=90)
        self.tree.column("#4", width=90)
        self.tree.column("#5", width=90)
        self.tree.column("#6", width=90)
        self.tree.column("#7", width=90)
        self.tree.column("#8", width=90)
        self.tree.column("#9", width=120)
        
    def create_buttons(self, frame):
        agregar_button = tk.Button(frame, text="Agregar", command=self.agregar, width=10)
        agregar_button.grid(row=10, column=0, pady=10)

        borrar_button = tk.Button(frame, text="Borrar", command=self.borrar_registro, width=10)
        borrar_button.grid(row=10, column=1)

        modificar_button = tk.Button(frame, text="Modificar", command=self.modificar_registro, width=10)
        modificar_button.grid(row=10, column=2, padx=10)

        boton_conectar = tk.Button(frame, text="Refresh", command=self.refresh, width=10)
        boton_conectar.grid(row=11, column=0, padx=10)
        
        consultar_button = tk.Button(frame, text="Consultar", command=self.consultar_datos, width=10)
        consultar_button.grid(row=11, column=1, padx=10)

        salir_button = tk.Button(frame, text="Salir", command=self.salir, bg="red", fg="black", width=10)
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
            cursor.execute("INSERT INTO personal (dni_personal, nombre_personal, apellido_personal, legajo, direccion, telefono, rol, fecha_nacimiento) "
                           "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                           (datos["DNI"], datos["Nombre"], datos["Apellido"], datos["Legajo"], datos["Direccion"], datos["Telefono"], datos["Rol"], datos["Fecha Nacimiento"]))
            self.conn.commit()
            messagebox.showinfo("Registro Agregado", "El registro se ha agregado correctamente.")
            self.load_data()
            self.clear_entries()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo agregar el registro:\n{str(e)}")

    def borrar_registro(self):
        id_personal_a_borrar = self.entry_vars["DNI"].get()

        if not id_personal_a_borrar:
            messagebox.showerror("Error", "Ingrese un id_personal para borrar un registro.")
            return

        try:
            cursor = self.conn.cursor()
            cursor.execute("DELETE FROM personal WHERE dni_personal=?", (id_personal_a_borrar,))
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
            keys_order = ["ID Personal", "DNI", "Nombre", "Apellido", "Legajo", "Direccion", "Telefono", "Rol", "Fecha Nacimiento"]

            for i, key in enumerate(keys_order):
                if i < len(values):
                    var = self.entry_vars[key]
                    var.set(values[i])
                else:
                    var = self.entry_vars[key]
                    var.set("")

    

    '''    
    def load_data_to_entries(self, event):
        selected_item = self.tree.selection()
        if selected_item:
            values = self.tree.item(selected_item, 'values')
            for i, var in enumerate(self.entry_vars.values()):
                var.set(values[i])
    '''

    def modificar_registro(self):
        datos = {label: var.get() for label, var in self.entry_vars.items()}
        id_personal_a_modificar = datos["ID Personal"]

        if not id_personal_a_modificar:
            messagebox.showerror("Error", "Ingrese un dni_personal para modificar un registro.")
            return

        try:
            cursor = self.conn.cursor()
            cursor.execute("UPDATE personal SET dni_personal=?, nombre_personal=?, apellido_personal=?, legajo=?, direccion=?, telefono=?, rol=?, fecha_nacimiento=? WHERE id_personal=?",
                           (datos["DNI"], datos["Nombre"], datos["Apellido"], datos["Legajo"], datos["Direccion"], datos["Telefono"], datos["Rol"], datos["Fecha Nacimiento"], id_personal_a_modificar))
            self.conn.commit()
            messagebox.showinfo("Registro Modificado", "El registro se ha modificado correctamente.")
            self.load_data()
            self.clear_entries()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo modificar el registro:\n{str(e)}")


            
    def consultar_datos(self):
    # Obtener el DNI del alumno a borrar desde el campo de entrada
        consulta = self.entry_vars["DNI"].get()

        if not consulta:
            messagebox.showerror("Error", "Ingrese un DNI para buscar un registro.")
            return

        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT id_personal, dni_personal, nombre_personal, apellido_personal, legajo, direccion, telefono, rol, fecha_nacimiento FROM personal WHERE dni_personal=?", (consulta,))
            result = cursor.fetchone()
            if result is not None:
                messagebox.showinfo("Registro encontrado", "El registro se ha encontrado correctamente.")
            # Mostrar el registro encontrado en la Treeview o en otro widget apropiado
            # Por ejemplo, si usas una Treeview llamada "self.treeview", puedes agregar una fila
            # con los datos encontrados de la siguiente manera:
                self.tree.delete(*self.tree.get_children())  # Limpiar la Treeview
                self.tree.insert("", "end", values=(result[0], result[1], result[2], result[3], result[4], result[5], result[6], result[7], result[8]))
            else:
                messagebox.showinfo("No se encontraron resultados", "No se encontraron registros con el DNI especificado.")

            
            #self.load_data()  # Recargar los datos en la Treeview después del borrado
            #self.clear_entries()
            
            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo borrar el registro:\n{str(e)}")
                    
    def refresh (self):
        self.load_data()
        self.clear_entries()

    
    def load_data(self):
        if self.conn is not None:
            cursor = self.conn.cursor()
            cursor.execute('SELECT id_personal, dni_personal, nombre_personal, apellido_personal, legajo, direccion, telefono, rol, fecha_nacimiento FROM personal')
            data = cursor.fetchall()
            self.clear_treeview()
            for row in data:
                self.tree.insert('', 'end', values=(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8]))

        

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
    app = PersonalApp(root)
    root.mainloop()
