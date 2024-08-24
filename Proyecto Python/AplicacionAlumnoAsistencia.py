import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import pyodbc
import pandas as pd

class AlumnoAsistenciaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Agenda Alumno E.E.T N°21")
        
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
        labels = ["id_alumno", "DNI", "Nombre", "Apellido", "CUIL", "Tutores", "Matrícula", "Teléfono", "Dirección", "Fecha Nacimiento"]
        self.entry_vars = {}
        for i, label_text in enumerate(labels):
            label = tk.Label(frame, text=label_text + ": ", bg="MediumSeaGreen")
            label.grid(row=i, column=0, sticky="e")

            entry_var = tk.StringVar()
            entry = tk.Entry(frame, textvariable=entry_var)
            entry.grid(row=i, column=1, padx=10, pady=5)
            self.entry_vars[label_text] = entry_var

    def create_treeview_widget(self, frame):
        self.tree = ttk.Treeview(frame, columns=("id_alumno", "DNI", "Nombre", "Apellido", "CUIL", "Tutores", "Matrícula", "Teléfono", "Dirección", "Fecha Nacimiento"))
        self.tree.heading("#1", text="id_alumno")
        self.tree.heading("#2", text="DNI")
        self.tree.heading("#3", text="Nombre")
        self.tree.heading("#4", text="Apellido")
        self.tree.heading("#5", text="CUIL")
        self.tree.heading("#6", text="Tutores")
        self.tree.heading("#7", text="Matrícula")
        self.tree.heading("#8", text="Teléfono")
        self.tree.heading("#9", text="Dirección")
        self.tree.heading("#10", text="Fecha Nacimiento")
        self.tree.grid()
        self.tree.column("#0", width=2)
        self.tree.column("#1", width=90)
        self.tree.column("#2", width=90)
        self.tree.column("#3", width=90)
        self.tree.column("#4", width=90)
        self.tree.column("#5", width=90)
        self.tree.column("#6", width=90)
        self.tree.column("#7", width=90)
        self.tree.column("#8", width=90)
        self.tree.column("#9", width=90)
        self.tree.column("#10", width=100)

    def create_buttons(self, frame):
        agregar_button = tk.Button(frame, text="Agregar Registro", command=self.agregar, height=2, width=15, bg="#98fb98")
        agregar_button.grid(row=10, column=1, pady=10)

        borrar_button = tk.Button(frame, text="Borrar", command=self.borrar_registro)
        borrar_button.grid(row=10, column=0)

        modificar_button = tk.Button(frame, text="Modificar", command=self.modificar_registro)
        modificar_button.grid(row=10, column=2, padx=10)

        boton_conectar = tk.Button(frame, text="SQL Server", command=self.connect_to_db)
        boton_conectar.grid(row=11, column=0, padx=10)

        boton_conectar = tk.Button(frame, text="Consulta", command=self.entry_vars)
        boton_conectar.grid(row=11, column=2, padx=11)

        salir_button = tk.Button(frame, text="Salir", command=self.salir, bg="red", fg="white", width=10)
        salir_button.grid(row=11, column=2, pady=10)

        # Agregar botón para registrar asistencia
        #registrar_asistencia_button = tk.Button(frame, text="Registrar Asistencia", command=self.registrar_asistencia)
        #registrar_asistencia_button.grid(row=12, column=0, columnspan=3, pady=10)

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
        # Obtener los datos ingresados en los cuadros de texto
        datos = {label: var.get() for label, var in self.entry_vars.items()}

        try:
            cursor = self.conn.cursor()
            cursor.execute("INSERT INTO alumnos (dni_alumno, nombre_alumno, apellido_alumno, CUIL_alumno, tutores, matricula, telefono_alumno, direccion_alumno, fecha_nacimiento_alumno) "
                           "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                           (datos["DNI"], datos["Nombre"], datos["Apellido"], datos["CUIL"], datos["Tutores"], datos["Matrícula"], datos["Teléfono"], datos["Dirección"], datos["Fecha Nacimiento"]))
            self.conn.commit()
            messagebox.showinfo("Registro Agregado", "El registro se ha agregado correctamente.")
            self.load_data()
            self.clear_entries()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo agregar el registro:\n{str(e)}")

    def load_data_to_entries(self, event):
        selected_item = self.tree.selection()
        if selected_item:
            values = self.tree.item(selected_item, 'values')
            keys_order = ["id_alumno", "DNI", "Nombre", "Apellido", "CUIL", "Tutores", "Matrícula", "Teléfono", "Dirección", "Fecha Nacimiento"]

            for i, key in enumerate(keys_order):
                if i < len(values):
                    var = self.entry_vars[key]
                    var.set(values[i])
                else:
                    var = self.entry_vars[key]
                    var.set("")

    def borrar_registro(self):
        # Obtener el DNI del alumno a borrar desde el campo de entrada
        dni_a_borrar = self.entry_vars["DNI"].get()

        if not dni_a_borrar:
            messagebox.showerror("Error", "Ingrese un DNI para borrar un registro.")
            return

        try:
            cursor = self.conn.cursor()
            cursor.execute("DELETE FROM alumnos WHERE dni_alumno=?", (dni_a_borrar,))
            self.conn.commit()
            messagebox.showinfo("Registro Borrado", "El registro se ha borrado correctamente.")
            self.load_data()  # Recargar los datos en la Treeview después del borrado
            self.clear_entries()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo borrar el registro:\n{str(e)}")

    def modificar_registro(self):
        # Obtener los datos ingresados en los cuadros de texto
        datos = {label: var.get() for label, var in self.entry_vars.items()}

        # Obtener el DNI del alumno a modificar desde el campo de entrada
        dni_a_modificar = datos["DNI"]

        if not dni_a_modificar:
            messagebox.showerror("Error", "Ingrese un DNI para modificar un registro.")
            return

        try:
            cursor = self.conn.cursor()
            cursor.execute("UPDATE alumnos SET nombre_alumno=?, apellido_alumno=?, CUIL_alumno=?, tutores=?, matricula=?, telefono_alumno=?, direccion_alumno=?, fecha_nacimiento_alumno=? WHERE dni_alumno=?",
                           (datos["Nombre"], datos["Apellido"], datos["CUIL"], datos["Tutores"], datos["Matrícula"], datos["Teléfono"], datos["Dirección"], datos["Fecha Nacimiento"], dni_a_modificar))
            self.conn.commit()
            messagebox.showinfo("Registro Modificado", "El registro se ha modificado correctamente.")
            self.load_data()  # Recargar los datos en la Treeview después de la modificación
            self.clear_entries()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo modificar el registro:\n{str(e)}")

    def consultar_datos(self):
        # Obtener el valor de la consulta ingresado en un campo de entrada
        consulta = self.entry_vars["Consulta"].get()

        if not consulta:
            messagebox.showerror("Error", "Ingrese una consulta SQL.")
            return

        try:
            cursor = self.conn.cursor()
            cursor.execute(consulta)
            data = cursor.fetchall()
            self.clear_treeview()

            if not data:
                messagebox.showinfo("Consulta", "No se encontraron resultados.")
            else:
                for row in data:
                    self.tree.insert('', 'end', values=row)

        except Exception as e:
            messagebox.showerror("Error", f"Error al ejecutar la consulta:\n{str(e)}")

    def load_data(self):
        if self.conn is not None:
            cursor = self.conn.cursor()
            cursor.execute('SELECT id_alumno, dni_alumno, nombre_alumno, apellido_alumno, CUIL_alumno, tutores, matricula, telefono_alumno, direccion_alumno, fecha_nacimiento_alumno FROM alumnos')
            data = cursor.fetchall()
            self.clear_treeview()
            for row in data:
                self.tree.insert('', 'end', values=(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9]))

    def clear_entries(self):
        for var in self.entry_vars.values():
            var.set("")
            
    def consultar_datos(self):
    # Obtener el valor de la consulta ingresado en un campo de entrada
        consulta = self.entry_vars["Consulta"].get()

        if not consulta:
            messagebox.showerror("Error", "Ingrese una consulta SQL.")
            return

        try:
            cursor = self.conn.cursor()
            cursor.execute(consulta)
            data = cursor.fetchall()
            self.clear_treeview()

            if not data:
                messagebox.showinfo("Consulta", "No se encontraron resultados.")
            else:
                for row in data:
                    self.tree.insert('', 'end', values=row)

        except Exception as e:
            messagebox.showerror("Error", f"Error al ejecutar la consulta:\n{str(e)}")

    def clear_treeview(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

    def registrar_asistencia(self):
        # Crea una nueva ventana para registrar la asistencia
        asistencia_window = tk.Toplevel(self.root)
        asistencia_window.title("Registro de Asistencia")

        # Agrega los campos necesarios para la asistencia
        tk.Label(asistencia_window, text="ID Asistencia:").pack()
        asistencia_var = tk.StringVar()
        asistencia_entry = tk.Entry(asistencia_window, textvariable=asistencia_var)
        asistencia_entry.pack()

        
        tk.Label(asistencia_window, text="Fecha:").pack()
        fecha_var = tk.StringVar()
        fecha_entry = tk.Entry(asistencia_window, textvariable=fecha_var)
        fecha_entry.pack()

        tk.Label(asistencia_window, text="Hora:").pack()
        hora_var = tk.StringVar()
        hora_entry = tk.Entry(asistencia_window, textvariable=hora_var)
        hora_entry.pack()

        tk.Label(asistencia_window, text="Condicion:").pack()
        condicion_var = tk.StringVar()
        condicion_entry = tk.Entry(asistencia_window, textvariable=condicion_var)
        condicion_entry.pack()

        tk.Label(asistencia_window, text="Cantidad de Asistencia:").pack()
        cantidadAsistencia_var = tk.StringVar()
        cantidadAsistencia_entry = tk.Entry(asistencia_window, textvariable=cantidadAsistencia_var)
        cantidadAsistencia_entry.pack()

        tk.Label(asistencia_window, text="Turno:").pack()
        turno_var = tk.StringVar()
        turno_entry = tk.Entry(asistencia_window, textvariable=turno_var)
        turno_entry.pack()

        tk.Label(asistencia_window, text="Reintegrado:").pack()
        reintegrado_var = tk.StringVar()
        reintegrado_entry = tk.Entry(asistencia_window, textvariable=reintegrado_var)
        reintegrado_entry.pack()

        tk.Label(asistencia_window, text="Evento:").pack()
        evento_var = tk.StringVar()
        evento_entry = tk.Entry(asistencia_window, textvariable=evento_var)
        evento_entry.pack()

        tk.Label(asistencia_window, text="ID Alumno").pack()
        alumno_var = tk.StringVar()
        alumno_entry = tk.Entry(asistencia_window, textvariable=alumno_var)
        alumno_entry.pack()

        # Agrega un botón para confirmar el registro de asistencia
        registrar_button = tk.Button(asistencia_window, text="Registrar", command=lambda: self.registrar_asistencia_alumno(asistencia_window, fecha_var, hora_var, condicion_var, cantidadAsistencia_var, turno_var, reintegrado_var, evento_var, alumno_var))
        registrar_button.pack()

    def registrar_asistencia_alumno(self, asistencia_window, fecha_var, hora_var, condicion_var, cantidadAsistencia_var, turno_var, reintegrado_var, evento_var, alumno_var):
        # Obtén los datos de asistencia ingresados en la ventana
        datos_asistencia = {
            "fecha": fecha_var.get(),
            "hora": hora_var.get(),
            "condicion": condicion_var.get(),
            "cantidad_asistencia": cantidadAsistencia_var.get(),
            "turno": turno_var.get(),
            "reintegrado": reintegrado_var.get(),
            "evento": evento_var.get(),
            "id_alumno": alumno_var.get()
        }

        try:
            cursor = self.conn.cursor()
            cursor.execute("INSERT INTO asistencia (fecha, hora, condicion, cantidad_asistencia, turno, reintegrado, evento, id_alumno) "
                           "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                           (datos_asistencia["fecha"], datos_asistencia["hora"], datos_asistencia["condicion"],
                            datos_asistencia["cantidad_asistencia"], datos_asistencia["turno"], datos_asistencia["reintegrado"],
                            datos_asistencia["evento"], datos_asistencia["id_alumno"]))
            self.conn.commit()
            messagebox.showinfo("Registro de Asistencia", "La asistencia se ha registrado correctamente.")
            asistencia_window.destroy()  # Cierra la ventana de registro de asistencia
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo registrar la asistencia:\n{str(e)}")

    def clear_treeview(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

    def salir(self):
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = AlumnoAsistenciaApp(root)
    root.mainloop()
