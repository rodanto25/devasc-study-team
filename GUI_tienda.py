# Rodrigo Antonio Estrada Orantes - GUI Tkinter
# https://github.com/rodanto25/devasc-study-team

import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

# Configuración de conexión
config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'oracle',
    'database': 'practica15_23270051'
}

def conectar():
    return mysql.connector.connect(**config)

class CRUDApp:
    def __init__(self, root):
        self.root = root
        self.root.title("tencno_tienda")
        self.root.geometry("1080x720")

        # Configurar el grid para expansión
        for i in range(6):
            root.grid_columnconfigure(i, weight=1)
        root.grid_rowconfigure(2, weight=1)

        # Combobox para seleccionar tabla
        
        self.tabla_var = tk.StringVar()
        self.tabla_combo = ttk.Combobox(root, textvariable=self.tabla_var, state="readonly")
        tk.Label(root, text="Elegir tabla:").grid(row=0, column=0, padx=10, pady=(10, 0), sticky="nw")
        self.tabla_combo['values'] = ('clientes', 'proveedor', 'productos', 'empleado')
        self.tabla_combo.grid(row=0, column=0, padx=90, pady=10, sticky="ew")
        self.tabla_combo.bind("<<ComboboxSelected>>", lambda e: self.cargar_datos())

        # Botón actualizar
        tk.Button(root, text="recargar", command=self.cargar_datos)\
            .grid(row=0, column=1, padx=5, pady=10, sticky="ew")

        # Búsqueda por ID
        self.buscar_id = tk.Entry(root)
        self.buscar_id.grid(row=0, column=3, padx=10, pady=10, sticky="ew")
        tk.Button(root, text="Buscar ID", command=self.buscar_por_id)\
            .grid(row=0, column=4, padx=5, pady=10, sticky="ew")

        # Botones CRUD organizados
        botones_frame = tk.Frame(root)
        botones_frame.grid(row=1, column=0, columnspan=5, pady=10, sticky="ew")
        botones_frame.grid_columnconfigure((0, 1, 2), weight=1)

        tk.Button(botones_frame, text="Crear", command=self.crear_registro)\
            .grid(row=0, column=0, padx=5, sticky="ew")
        tk.Button(botones_frame, text="Actualizar", command=self.actualizar_registro)\
            .grid(row=0, column=1, padx=5, sticky="ew")
        tk.Button(botones_frame, text="Eliminar", command=self.eliminar_registro)\
            .grid(row=0, column=2, padx=5, sticky="ew")

        # Treeview
        self.tree = ttk.Treeview(root)
        self.tree.grid(row=2, column=0, columnspan=5, sticky="nsew", padx=10, pady=10)

        # Scrollbar
        scrollbar = ttk.Scrollbar(root, orient="vertical", command=self.tree.yview)
        scrollbar.grid(row=2, column=5, sticky="ns")
        self.tree.configure(yscrollcommand=scrollbar.set)

    def ventana_confirmacion(self, mensaje, callback_si):
        top = tk.Toplevel(self.root)
        top.title("Confirmar operación")
        top.geometry("300x150")
        top.grab_set()  # Bloquea la ventana principal hasta que se cierre esta

        tk.Label(top, text=mensaje, wraplength=280, fg="red", font=("Arial", 12, "bold")).pack(pady=20)

        boton_frame = tk.Frame(top)
        boton_frame.pack(pady=10)

        def confirmar():
            top.destroy()
            callback_si()

        def cancelar():
            top.destroy()

        tk.Button(boton_frame, text="Aceptar", command=confirmar, bg="green", fg="white", width=10).pack(side="left", padx=10)
        tk.Button(boton_frame, text="Cancelar", command=cancelar, bg="gray", fg="white", width=10).pack(side="right", padx=10)

    def cargar_datos(self):
        tabla = self.tabla_var.get()
        if not tabla:
            return

        # Limpiar datos actuales
        self.tree.delete(*self.tree.get_children())

        # Obtener datos desde la base
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {tabla}")
        columnas = [i[0] for i in cursor.description]

        # Configurar columnas en el Treeview
        self.tree['columns'] = columnas
        self.tree['show'] = 'headings'

        for col in columnas:
            self.tree.heading(col, text=col, anchor='center')  # Centrar encabezado
            self.tree.column(col, anchor='center')              # Centrar datos

        # Insertar filas
        for fila in cursor.fetchall():
            self.tree.insert('', 'end', values=fila)

        cursor.close()
        conn.close()

        # Ajustar el ancho automaticamente
        for col in columnas:
            # Calcular ancho máximo del contenido
            max_width = max(
                [len(str(self.tree.set(child, col))) for child in self.tree.get_children()] + [len(col)]
            )
            self.tree.column(col, width=(max_width * 10))  # Puedes ajustar el multiplicador

    def crear_registro(self):
        tabla = self.tabla_var.get()
        if tabla == 'clientes':
            self.ventana_cliente()
        elif tabla == 'proveedor':
            self.ventana_proveedor()
        elif tabla == 'productos':
            self.ventana_producto()
        elif tabla == 'empleado':
            self.formulario_empleado()
    
    def ventana_editar_cliente(self, id_valor, item):
        top = tk.Toplevel(self.root)
        top.title("Editar Cliente")
        w, h = 300, 200
        top.geometry(f"{w}x{h}")

        top.update_idletasks()
        x = self.root.winfo_x() + (self.root.winfo_width() // 2) - (w // 2)
        y = self.root.winfo_y() + (self.root.winfo_height() // 2) - (h // 2)
        top.geometry(f"{w}x{h}+{x}+{y}")

        # Campos para editar (solo ejemplo con 2 campos: nombre y teléfono)
        tk.Label(top, text="Nombre:").pack()
        nombre = tk.Entry(top)
        nombre.insert(0, item[1])  # Rellenar con el valor actual
        nombre.pack()

        tk.Label(top, text="Teléfono:").pack()
        telefono = tk.Entry(top)
        telefono.insert(0, item[2])  # Rellenar con el valor actual
        telefono.pack()

        def guardar():
            try:
                if not nombre.get() or not telefono.get():
                    raise ValueError("Todos los campos son obligatorios.")

                # Actualizar el registro en la base de datos
                conn = conectar()
                cursor = conn.cursor()
                cursor.execute("UPDATE clientes SET nombre = %s, telefono = %s WHERE id_cliente = %s",
                            (nombre.get(), telefono.get(), id_valor))
                conn.commit()
                cursor.close()
                conn.close()
                top.destroy()
                self.cargar_datos()  # Recargar los datos actualizados
            except Exception as e:
                messagebox.showerror("Error", f"Verifica los datos ingresados.\n{e}")

        tk.Button(top, text="Guardar", command=guardar).pack()
    
    def ventana_editar_proveedor(self, id_valor, item):
        top = tk.Toplevel(self.root)
        top.title("Editar Proveedor")
        w, h = 300, 200
        top.geometry(f"{w}x{h}")

        top.update_idletasks()
        x = self.root.winfo_x() + (self.root.winfo_width() // 2) - (w // 2)
        y = self.root.winfo_y() + (self.root.winfo_height() // 2) - (h // 2)
        top.geometry(f"{w}x{h}+{x}+{y}")

        campos = ["Nombre", "Teléfono", "Dirección", "Correo"]
        entradas = {}

        for i, campo in enumerate(campos):
            tk.Label(top, text=f"{campo}:").pack()
            entrada = tk.Entry(top)
            entrada.insert(0, item[i+1])  # Rellenar con el valor actual
            entrada.pack()
            entradas[campo] = entrada

        def guardar():
            try:
                datos = tuple(entradas[c].get() for c in campos)
                if any(not d for d in datos):
                    raise ValueError("Todos los campos son obligatorios.")

                conn = conectar()
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE proveedor SET nombre = %s, telefono = %s, direccion = %s, correo = %s
                    WHERE id_proveedor = %s
                """, (*datos, id_valor))
                conn.commit()
                cursor.close()
                conn.close()
                top.destroy()
                self.cargar_datos()  # Recargar los datos actualizados
            except Exception as e:
                messagebox.showerror("Error", f"Verifica los datos ingresados.\n{e}")

        tk.Button(top, text="Guardar", command=guardar).pack()

    def ventana_editar_producto(self, id_valor, item):
        top = tk.Toplevel(self.root)
        top.title("Editar Producto")
        w, h = 300, 250
        top.geometry(f"{w}x{h}")

        top.update_idletasks()
        x = self.root.winfo_x() + (self.root.winfo_width() // 2) - (w // 2)
        y = self.root.winfo_y() + (self.root.winfo_height() // 2) - (h // 2)
        top.geometry(f"{w}x{h}+{x}+{y}")

        campos = ["Nombre", "Descripción", "Precio", "Stock", "ID Proveedor"]
        entradas = {}

        for campo in campos:
            tk.Label(top, text=f"{campo}:").pack()
            entradas[campo] = tk.Entry(top)
            entradas[campo].insert(0, item[campos.index(campo) + 1])  # Rellenar con el valor actual
            entradas[campo].pack()

        def guardar():
            try:
                nombre = entradas["Nombre"].get()
                descripcion = entradas["Descripción"].get()
                precio = float(entradas["Precio"].get())
                stock = int(entradas["Stock"].get())
                id_proveedor = int(entradas["ID Proveedor"].get())

                conn = conectar()
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE productos SET nombre = %s, descripcion = %s, precio = %s, stock = %s, id_proveedor = %s
                    WHERE id_producto = %s
                """, (nombre, descripcion, precio, stock, id_proveedor, id_valor))
                conn.commit()
                cursor.close()
                conn.close()
                top.destroy()
                self.cargar_datos()  # Recargar los datos actualizados
            except Exception as e:
                messagebox.showerror("Error", f"Verifica los datos ingresados.\n{e}")

        tk.Button(top, text="Guardar", command=guardar).pack()

    def ventana_editar_empleado(self, id_valor, item):
        top = tk.Toplevel(self.root)
        top.title("Editar Empleado")
        w, h = 300, 250
        top.geometry(f"{w}x{h}")

        top.update_idletasks()
        x = self.root.winfo_x() + (self.root.winfo_width() // 2) - (w // 2)
        y = self.root.winfo_y() + (self.root.winfo_height() // 2) - (h // 2)
        top.geometry(f"{w}x{h}+{x}+{y}")

        campos = ["correo", "contrasena", "puesto"]
        entradas = {}

        for campo in campos:
            tk.Label(top, text=f"{campo}:").pack()
            entrada = tk.Entry(top)
            entrada.insert(0, item[campos.index(campo) + 1])  # Rellenar con el valor actual
            entrada.pack()
            entradas[campo] = entrada

        def guardar():
            try:
                datos = tuple(entradas[c].get() for c in campos)
                if any(not d for d in datos):
                    raise ValueError("Todos los campos son obligatorios.")

                # Actualizar el registro en la base de datos
                conn = conectar()
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE empleado SET correo = %s, contrasena = %s, puesto = %s
                    WHERE id_empleado = %s
                """, (*datos, id_valor))
                conn.commit()
                cursor.close()
                conn.close()
                top.destroy()
                self.cargar_datos()  # Recargar los datos actualizados
            except Exception as e:
                messagebox.showerror("Error", f"Verifica los datos ingresados.\n{e}")

        tk.Button(top, text="Guardar", command=guardar).pack()



    def actualizar_registro(self):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Atención", "Selecciona un registro para actualizar.")
            return

        # Obtener los valores del registro seleccionado
        item = self.tree.item(seleccion[0])['values']
        tabla = self.tabla_var.get()
        id_campo = 'id_' + tabla[:-1] if tabla != 'productos' else 'id_producto'
        id_valor = item[0]  # Suponiendo que el ID es el primer valor del registro

        # Abrir el formulario para editar según la tabla seleccionada
        if tabla == 'clientes':
            self.ventana_editar_cliente(id_valor, item)
        elif tabla == 'proveedor':
            self.ventana_editar_proveedor(id_valor, item)
        elif tabla == 'productos':
            self.ventana_editar_producto(id_valor, item)
        elif tabla == 'empleado':
            self.ventana_editar_empleado(id_valor, item) # Puedes extender esto si deseas lógica específica de edición

    def eliminar_registro(self):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Atención", "Selecciona un registro para eliminar.")
            return

        item = self.tree.item(seleccion[0])['values']
        id_campo = item[0]  # El ID del registro seleccionado
        tabla = self.tabla_var.get()

        # Determinar el nombre del campo de ID dependiendo de la tabla seleccionada
        if tabla == 'clientes':
            campo_id = 'id_cliente'  # Columna para clientes
        elif tabla == 'proveedor':
            campo_id = 'id_proveedor'  # Columna para proveedor
        elif tabla == 'productos':
            campo_id = 'id_producto'  # Columna para productos
        elif tabla == 'empleado':
            campo_id = 'id_empleado'  # Columna para empleados
        else:
            messagebox.showerror("Error", "Tabla no reconocida.")
            return

        # Confirmación antes de eliminar
        self.ventana_confirmacion(
            f"¿Estás seguro de que deseas eliminar este {tabla[:-1]}?",  # Mensaje con el nombre de la tabla
            lambda: self.procesar_eliminacion(tabla, campo_id, id_campo)
    )
    def ventana_confirmacion(self, mensaje, accion_confirmar):
        top = tk.Toplevel(self.root)
        top.title("Confirmar eliminación")
        w, h = 300, 150
        top.geometry(f"{w}x{h}")

        # Centrar ventana respecto a self.root
        top.update_idletasks()
        x = self.root.winfo_x() + (self.root.winfo_width() // 2) - (w // 2)
        y = self.root.winfo_y() + (self.root.winfo_height() // 2) - (h // 2)
        top.geometry(f"{w}x{h}+{x}+{y}")

        # Contenido
        tk.Label(top, text=mensaje, wraplength=280, justify="center").pack(pady=20)

        frame = tk.Frame(top)
        frame.pack()

        tk.Button(frame, text="Cancelar", command=top.destroy).pack(side="left", padx=10)
        tk.Button(frame, text="Confirmar", command=lambda: [accion_confirmar(), top.destroy()]).pack(side="left", padx=10)


    def procesar_eliminacion(self, tabla, campo_id, id_valor):
        try:
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute(f"DELETE FROM {tabla} WHERE {campo_id} = %s", (id_valor,))
            conn.commit()
            cursor.close()
            conn.close()
            self.cargar_datos()  # Recargar los datos después de la eliminación
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo eliminar el registro.\n{e}")


    def buscar_por_id(self):
        tabla = self.tabla_var.get()
        id_valor = self.buscar_id.get()

        if not id_valor:
            messagebox.showinfo("Aviso", "Introduce un ID para buscar.")
            return

        # Diccionario con los campos ID correctos por tabla
        campos_id = {
            'clientes': 'id_cliente',
            'proveedor': 'id_proveedor',
            'empleado': 'id_empleado',
            'productos': 'id_producto'}

        campo_id = campos_id.get(tabla)
        if not campo_id:
            messagebox.showerror("Error", f"No se reconoce la tabla '{tabla}'.")
            return

        try:
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM {tabla} WHERE {campo_id} = %s", (id_valor,))
            datos = cursor.fetchone()
            self.tree.delete(*self.tree.get_children())

            if datos:
                columnas = [i[0] for i in cursor.description]
                self.tree['columns'] = columnas
                self.tree['show'] = 'headings'
                for col in columnas:
                    self.tree.heading(col, text=col)
                    self.tree.column(col, anchor='center')  # Centra columnas
                self.tree.insert('', 'end', values=datos)
            else:
                messagebox.showinfo("Resultado", "No se encontró el registro.")

            cursor.close()
            conn.close()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo realizar la búsqueda.\n{e}")

    def ventana_cliente(self):
        top = tk.Toplevel(self.root)
        top.title("Agregar Cliente")
        w, h= 300, 200
        top.geometry(f"{w}x{h}")
        
        top.update_idletasks()
        x = self.root.winfo_x() + (self.root.winfo_width() // 2) - (w // 2)
        y = self.root.winfo_y() + (self.root.winfo_height() // 2) - (h // 2)
        top.geometry(f"{w}x{h}+{x}+{y}")
    
        tk.Label(top, text="Nombre:").pack()
        nombre = tk.Entry(top)
        nombre.pack()

        tk.Label(top, text="Teléfono:").pack()
        telefono = tk.Entry(top)
        telefono.pack()

        def guardar():
            try:
                if not nombre.get() or not telefono.get():
                    raise ValueError("Todos los campos son obligatorios.")

                conn = conectar()
                cursor = conn.cursor()
                cursor.execute("INSERT INTO clientes (nombre, telefono) VALUES (%s, %s)", (nombre.get(), telefono.get()))
                conn.commit()
                cursor.close()
                conn.close()
                top.destroy()
                self.cargar_datos()
            except Exception as e:
                messagebox.showerror("Error", f"Verifica los datos ingresados.\n{e}")

        tk.Button(top, text="Guardar", command=guardar).pack()

    def ventana_proveedor(self):
        top = tk.Toplevel(self.root)
        top.title("Agregar Proveedor")
        w, h= 300, 200
        top.geometry(f"{w}x{h}")
        
        top.update_idletasks()
        x = self.root.winfo_x() + (self.root.winfo_width() // 2) - (w // 2)
        y = self.root.winfo_y() + (self.root.winfo_height() // 2) - (h // 2)
        top.geometry(f"{w}x{h}+{x}+{y}")
        
        campos = {}
        for etiqueta in ("Nombre", "Teléfono", "Dirección", "Correo"):
            tk.Label(top, text=f"{etiqueta}:").pack()
            entrada = tk.Entry(top)
            entrada.pack()
            campos[etiqueta.lower()] = entrada

        def guardar():
            try:
                datos = tuple(campos[c].get() for c in ("nombre", "teléfono", "dirección", "correo"))
                if any(not d for d in datos):
                    raise ValueError("Todos los campos son obligatorios.")
                conn = conectar()
                cursor = conn.cursor()
                cursor.execute("INSERT INTO proveedor (nombre, telefono, direccion, correo) VALUES (%s, %s, %s, %s)", datos)
                conn.commit()
                cursor.close()
                conn.close()
                top.destroy()
                self.cargar_datos()
            except Exception as e:
                messagebox.showerror("Error", f"Verifica los datos ingresados.\n{e}")

        tk.Button(top, text="Guardar", command=guardar).pack()

    def ventana_producto(self):
        top = tk.Toplevel(self.root)
        top.title("Agregar Producto")
        w, h= 300, 250
        top.geometry(f"{w}x{h}")
        
        top.update_idletasks()
        x = self.root.winfo_x() + (self.root.winfo_width() // 2) - (w // 2)
        y = self.root.winfo_y() + (self.root.winfo_height() // 2) - (h // 2)
        top.geometry(f"{w}x{h}+{x}+{y}")
        
        campos = ["Nombre", "Descripción", "Precio", "Stock", "ID Proveedor"]
        entradas = {}
        for campo in campos:
            tk.Label(top, text=f"{campo}:").pack()
            entradas[campo] = tk.Entry(top)
            entradas[campo].pack()

        def guardar():
            try:
                nombre = entradas["Nombre"].get()
                descripcion = entradas["Descripción"].get()
                precio = float(entradas["Precio"].get())
                stock = int(entradas["Stock"].get())
                id_proveedor = entradas["ID Proveedor"].get()
                id_proveedor = int(id_proveedor) if id_proveedor else None

                if not nombre or not descripcion:
                    raise ValueError("Nombre y descripción son obligatorios.")

                conn = conectar()
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO productos (nombre, descripcion, precio, stock, id_proveedor)
                    VALUES (%s, %s, %s, %s, %s)
                """, (nombre, descripcion, precio, stock, id_proveedor))
                conn.commit()
                cursor.close()
                conn.close()
                top.destroy()
                self.cargar_datos()
            except ValueError as ve:
                messagebox.showerror("Error", f"{ve}")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo guardar el producto.\n{e}")

        tk.Button(top, text="Guardar", command=guardar).pack()
        
    def formulario_empleado(self):
        top = tk.Toplevel(self.root)
        top.title("Agregar Empleado")
        w, h= 300, 200
        top.geometry(f"{w}x{h}")
        
        top.update_idletasks()
        x = self.root.winfo_x() + (self.root.winfo_width() // 2) - (w // 2)
        y = self.root.winfo_y() + (self.root.winfo_height() // 2) - (h // 2)
        top.geometry(f"{w}x{h}+{x}+{y}")
        
        campos = {"Correo": None, "Contraseña": None, "Puesto": None}
        entradas = {}

        for campo in campos:
            tk.Label(top, text=f"{campo}:").pack()
            entrada = tk.Entry(top)
            entrada.pack()
            entradas[campo] = entrada

        def guardar():
            try:
                correo = entradas["Correo"].get()
                contrasena = entradas["Contraseña"].get()
                puesto = entradas["Puesto"].get()

                if not correo or not contrasena or not puesto:
                    raise ValueError("Todos los campos son obligatorios.")

                conn = conectar()
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO empleado (correo, contrasena, puesto) VALUES (%s, %s, %s)",
                    (correo, contrasena, puesto)
                )
                conn.commit()
                cursor.close()
                conn.close()
                top.destroy()
                self.cargar_datos()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo guardar el empleado.\n{e}")

        tk.Button(top, text="Guardar", command=guardar).pack()


if __name__ == "__main__":
    root = tk.Tk()
    app = CRUDApp(root)
    root.mainloop()
