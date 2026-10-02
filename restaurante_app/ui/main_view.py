import tkinter as tk
from pathlib import Path
from tkinter import messagebox, ttk
from typing import Callable, Dict, Optional

from modelos.usuario import Usuario
from servicios.restaurante_servicio import RestauranteServicio

CATEGORIAS = ("Platillo", "Bebida", "Postre")
ROLES = ("Administrador", "Empleado", "Cliente")
CARPETA_ASSETS: Path = Path(__file__).resolve().parent.parent / "assets"


class MainView(ttk.Frame):
    def __init__(self, contenedor: tk.Widget, servicio: RestauranteServicio,
                 al_cerrar_sesion: Callable[[], None]) -> None:
        super().__init__(contenedor, padding=10)
        self.servicio: RestauranteServicio = servicio
        self.al_cerrar_sesion: Callable[[], None] = al_cerrar_sesion
        self.usuario_actual: Optional[Usuario] = None
        self.tabla_usuarios: Optional[ttk.Treeview] = None

        self.__cargar_iconos()

        self.variable_codigo = tk.StringVar()
        self.variable_nombre = tk.StringVar()
        self.variable_categoria = tk.StringVar()
        self.variable_precio = tk.StringVar()
        self.variable_stock = tk.StringVar()
        self.variable_mensaje = tk.StringVar()

        self.variable_usuario_venta = tk.StringVar()
        self.variable_producto_venta = tk.StringVar()
        self.variable_mensaje_venta = tk.StringVar()

        self.mapa_usuarios_venta: Dict[str, str] = {}
        self.mapa_productos_venta: Dict[str, str] = {}

        self.__construir_encabezado()
        self.__construir_navegacion()
        self.__construir_barra_estado()

    # ------------------------------------------------------------------
    # Construcción general
    # ------------------------------------------------------------------
    def __cargar_iconos(self) -> None:
        self.iconos: Dict[str, tk.PhotoImage] = {}
        archivos = {
            "logo": "logo.png",
            "productos": "icono_productos.png",
            "usuarios": "icono_usuarios.png",
            "ventas": "icono_ventas.png",
        }
        for clave, nombre_archivo in archivos.items():
            ruta = CARPETA_ASSETS / nombre_archivo
            try:
                self.iconos[clave] = tk.PhotoImage(file=str(ruta))
            except tk.TclError:
                self.iconos[clave] = None

    def __construir_encabezado(self) -> None:
        marco_encabezado = ttk.Frame(self)
        marco_encabezado.pack(fill="x", pady=(0, 10))

        marco_titulo = ttk.Frame(marco_encabezado)
        marco_titulo.pack(side="left")

        if self.iconos.get("logo") is not None:
            logo_reducido = self.iconos["logo"].subsample(6, 6)
            self.iconos["logo_reducido"] = logo_reducido
            ttk.Label(marco_titulo, image=logo_reducido).pack(side="left", padx=(0, 10))

        ttk.Label(
            marco_titulo, text="Restaurante JoelFood", font=("Arial", 16, "bold")
        ).pack(side="left")

        ttk.Button(
            marco_encabezado, text="Cerrar sesión", command=self.al_cerrar_sesion
        ).pack(side="right")

    def __construir_navegacion(self) -> None:
        self.navegador = ttk.Notebook(self)
        self.navegador.pack(fill="both", expand=True)

        self.pestana_productos = ttk.Frame(self.navegador, padding=10)
        self.pestana_usuarios = ttk.Frame(self.navegador, padding=10)
        self.pestana_ventas = ttk.Frame(self.navegador, padding=10)

        self.navegador.add(self.pestana_productos, text="Productos", image=self.iconos.get("productos"), compound="left")
        self.navegador.add(self.pestana_usuarios, text="Usuarios", image=self.iconos.get("usuarios"), compound="left")
        self.navegador.add(self.pestana_ventas, text="Ventas", image=self.iconos.get("ventas"), compound="left")

        self.__construir_seccion_productos()
        # La sección de Usuarios se construye en establecer_usuario_actual(),
        # ya que su contenido depende del rol de la persona autenticada.
        self.__construir_seccion_ventas()

    def __construir_barra_estado(self) -> None:
        marco_estado = ttk.Frame(self)
        marco_estado.pack(fill="x", pady=(10, 0))

        self.etiqueta_mensaje = ttk.Label(marco_estado, textvariable=self.variable_mensaje)
        self.etiqueta_mensaje.pack(side="left")

    # ------------------------------------------------------------------
    # Sección Productos (desarrollada en semanas anteriores)
    # ------------------------------------------------------------------
    def __construir_seccion_productos(self) -> None:
        marco_formulario = ttk.LabelFrame(
            self.pestana_productos, text="Datos del producto", padding=10
        )
        marco_formulario.pack(fill="x")

        ttk.Label(marco_formulario, text="Código:").grid(row=0, column=0, sticky="w", padx=5, pady=4)
        ttk.Entry(marco_formulario, textvariable=self.variable_codigo, width=18).grid(
            row=0, column=1, padx=5, pady=4
        )

        ttk.Label(marco_formulario, text="Nombre:").grid(row=0, column=2, sticky="w", padx=5, pady=4)
        ttk.Entry(marco_formulario, textvariable=self.variable_nombre, width=28).grid(
            row=0, column=3, padx=5, pady=4
        )

        ttk.Label(marco_formulario, text="Categoría:").grid(row=1, column=0, sticky="w", padx=5, pady=4)
        ttk.Combobox(
            marco_formulario, textvariable=self.variable_categoria,
            values=CATEGORIAS, state="readonly", width=15
        ).grid(row=1, column=1, padx=5, pady=4)

        ttk.Label(marco_formulario, text="Precio:").grid(row=1, column=2, sticky="w", padx=5, pady=4)
        ttk.Entry(marco_formulario, textvariable=self.variable_precio, width=12).grid(
            row=1, column=3, sticky="w", padx=5, pady=4
        )

        ttk.Label(marco_formulario, text="Stock:").grid(row=2, column=0, sticky="w", padx=5, pady=4)
        ttk.Entry(marco_formulario, textvariable=self.variable_stock, width=12).grid(
            row=2, column=1, sticky="w", padx=5, pady=4
        )

        marco_acciones = ttk.LabelFrame(self.pestana_productos, text="Acciones", padding=10)
        marco_acciones.pack(fill="x", pady=10)

        ttk.Button(marco_acciones, text="Registrar", command=self.registrar_producto).pack(side="left", padx=4)
        ttk.Button(marco_acciones, text="Cargar", command=self.cargar_producto).pack(side="left", padx=4)
        ttk.Button(marco_acciones, text="Actualizar", command=self.actualizar_producto).pack(side="left", padx=4)
        ttk.Button(marco_acciones, text="Eliminar", command=self.eliminar_producto).pack(side="left", padx=4)
        ttk.Button(marco_acciones, text="Limpiar", command=self.limpiar_formulario).pack(side="left", padx=4)

        marco_tabla = ttk.LabelFrame(self.pestana_productos, text="Productos registrados", padding=10)
        marco_tabla.pack(fill="both", expand=True)

        columnas = ("codigo", "nombre", "categoria", "precio", "stock")
        self.tabla_productos = ttk.Treeview(marco_tabla, columns=columnas, show="headings", height=8)
        for columna, titulo, ancho in (
            ("codigo", "Código", 80),
            ("nombre", "Nombre", 220),
            ("categoria", "Categoría", 100),
            ("precio", "Precio", 80),
            ("stock", "Stock", 70),
        ):
            self.tabla_productos.heading(columna, text=titulo)
            self.tabla_productos.column(columna, width=ancho, anchor="w")

        barra_desplazamiento = ttk.Scrollbar(marco_tabla, orient="vertical", command=self.tabla_productos.yview)
        self.tabla_productos.configure(yscrollcommand=barra_desplazamiento.set)

        self.tabla_productos.pack(side="left", fill="both", expand=True)
        barra_desplazamiento.pack(side="right", fill="y")

    def registrar_producto(self) -> None:
        exitoso, mensaje = self.servicio.registrar_producto(
            self.variable_codigo.get(), self.variable_nombre.get(), self.variable_categoria.get(),
            self.variable_precio.get(), self.variable_stock.get(),
        )
        self.mostrar_mensaje(mensaje, exitoso)
        if exitoso:
            self.refrescar_productos()
            self.limpiar_formulario()

    def cargar_producto(self) -> None:
        producto = self.servicio.buscar_producto(self.variable_codigo.get())
        if producto is None:
            self.mostrar_mensaje("No se encontró un producto con ese código.", False)
            return
        self.variable_nombre.set(producto.nombre)
        self.variable_categoria.set(producto.categoria)
        self.variable_precio.set(f"{producto.precio:.2f}")
        self.variable_stock.set(str(producto.stock))
        self.mostrar_mensaje(f"Producto '{producto.codigo}' cargado en el formulario.", True)

    def actualizar_producto(self) -> None:
        exitoso, mensaje = self.servicio.actualizar_producto(
            self.variable_codigo.get(), self.variable_nombre.get(), self.variable_categoria.get(),
            self.variable_precio.get(), self.variable_stock.get(),
        )
        self.mostrar_mensaje(mensaje, exitoso)
        if exitoso:
            self.refrescar_productos()

    def eliminar_producto(self) -> None:
        exitoso, mensaje = self.servicio.eliminar_producto(self.variable_codigo.get())
        self.mostrar_mensaje(mensaje, exitoso)
        if exitoso:
            self.refrescar_productos()
            self.limpiar_formulario()

    def limpiar_formulario(self) -> None:
        self.variable_codigo.set("")
        self.variable_nombre.set("")
        self.variable_categoria.set("")
        self.variable_precio.set("")
        self.variable_stock.set("")

    def refrescar_productos(self) -> None:
        for fila in self.tabla_productos.get_children():
            self.tabla_productos.delete(fila)
        for producto in self.servicio.listar_productos():
            self.tabla_productos.insert(
                "", tk.END,
                values=(producto.codigo, producto.nombre, producto.categoria,
                        f"{producto.precio:.2f}", producto.stock),
            )
        self.refrescar_combos_venta()

    def mostrar_mensaje(self, mensaje: str, exitoso: bool) -> None:
        self.variable_mensaje.set(mensaje)
        self.etiqueta_mensaje.configure(foreground="green" if exitoso else "red")

    # ------------------------------------------------------------------
    # Sección Usuarios (evolución de la Semana 16)
    # ------------------------------------------------------------------
    def establecer_usuario_actual(self, usuario: Usuario) -> None:
        self.usuario_actual = usuario
        self.__reconstruir_seccion_usuarios()

    def __reconstruir_seccion_usuarios(self) -> None:
        for hijo in self.pestana_usuarios.winfo_children():
            hijo.destroy()
        self.tabla_usuarios = None

        if self.usuario_actual is not None and self.servicio.es_administrador(self.usuario_actual):
            self.__construir_gestion_usuarios()
        else:
            ttk.Label(
                self.pestana_usuarios,
                text="Esta sección está disponible únicamente para usuarios con rol Administrador.",
                font=("Arial", 11),
                wraplength=500,
                justify="center",
            ).pack(pady=60)

    def __construir_gestion_usuarios(self) -> None:
        self.variable_identificacion_usuario = tk.StringVar()
        self.variable_nombre_persona = tk.StringVar()
        self.variable_login_usuario = tk.StringVar()
        self.variable_contrasena_usuario = tk.StringVar()
        self.variable_rol_usuario = tk.StringVar()
        self.variable_mensaje_usuarios = tk.StringVar()

        marco_formulario = ttk.LabelFrame(self.pestana_usuarios, text="Datos del usuario", padding=10)
        marco_formulario.pack(fill="x")

        ttk.Label(marco_formulario, text="Identificación:").grid(row=0, column=0, sticky="w", padx=5, pady=4)
        entrada_identificacion = ttk.Entry(marco_formulario, textvariable=self.variable_identificacion_usuario, width=16)
        entrada_identificacion.grid(row=0, column=1, padx=5, pady=4)

        ttk.Label(marco_formulario, text="Nombre:").grid(row=0, column=2, sticky="w", padx=5, pady=4)
        entrada_nombre = ttk.Entry(marco_formulario, textvariable=self.variable_nombre_persona, width=26)
        entrada_nombre.grid(row=0, column=3, padx=5, pady=4)

        ttk.Label(marco_formulario, text="Usuario:").grid(row=1, column=0, sticky="w", padx=5, pady=4)
        entrada_login = ttk.Entry(marco_formulario, textvariable=self.variable_login_usuario, width=16)
        entrada_login.grid(row=1, column=1, padx=5, pady=4)

        ttk.Label(marco_formulario, text="Contraseña:").grid(row=1, column=2, sticky="w", padx=5, pady=4)
        entrada_contrasena = ttk.Entry(marco_formulario, textvariable=self.variable_contrasena_usuario, width=18)
        entrada_contrasena.grid(row=1, column=3, sticky="w", padx=5, pady=4)

        ttk.Label(marco_formulario, text="Rol:").grid(row=2, column=0, sticky="w", padx=5, pady=4)
        combo_rol = ttk.Combobox(
            marco_formulario, textvariable=self.variable_rol_usuario,
            values=ROLES, state="readonly", width=16
        )
        combo_rol.grid(row=2, column=1, sticky="w", padx=5, pady=4)

        # Evento <<ComboboxSelected>>: responde al cambio de rol.
        combo_rol.bind("<<ComboboxSelected>>", self.al_cambiar_rol)

        # Evento de teclado <Return>: reutiliza registrar_usuario() (sin duplicar lógica).
        # Evento de teclado <Escape>: reutiliza limpiar_formulario_usuario().
        for widget in (entrada_identificacion, entrada_nombre, entrada_login, entrada_contrasena, combo_rol):
            widget.bind("<Return>", self.manejar_enter_usuario)
            widget.bind("<Escape>", self.manejar_escape_usuario)

        marco_acciones = ttk.LabelFrame(self.pestana_usuarios, text="Acciones", padding=10)
        marco_acciones.pack(fill="x", pady=10)

        ttk.Button(marco_acciones, text="Registrar", command=self.registrar_usuario).pack(side="left", padx=4)
        ttk.Button(marco_acciones, text="Actualizar", command=self.actualizar_usuario).pack(side="left", padx=4)
        ttk.Button(marco_acciones, text="Eliminar", command=self.eliminar_usuario).pack(side="left", padx=4)
        ttk.Button(marco_acciones, text="Limpiar", command=self.limpiar_formulario_usuario).pack(side="left", padx=4)

        self.etiqueta_mensaje_usuarios = ttk.Label(marco_acciones, textvariable=self.variable_mensaje_usuarios)
        self.etiqueta_mensaje_usuarios.pack(side="left", padx=15)

        marco_tabla = ttk.LabelFrame(self.pestana_usuarios, text="Usuarios registrados", padding=10)
        marco_tabla.pack(fill="both", expand=True)

        columnas = ("identificacion", "nombre", "nombre_usuario", "rol")
        self.tabla_usuarios = ttk.Treeview(marco_tabla, columns=columnas, show="headings", height=8)
        for columna, titulo, ancho in (
            ("identificacion", "Identificación", 110),
            ("nombre", "Nombre", 200),
            ("nombre_usuario", "Usuario", 130),
            ("rol", "Rol", 120),
        ):
            self.tabla_usuarios.heading(columna, text=titulo)
            self.tabla_usuarios.column(columna, width=ancho, anchor="w")

        barra_desplazamiento = ttk.Scrollbar(marco_tabla, orient="vertical", command=self.tabla_usuarios.yview)
        self.tabla_usuarios.configure(yscrollcommand=barra_desplazamiento.set)

        self.tabla_usuarios.pack(side="left", fill="both", expand=True)
        barra_desplazamiento.pack(side="right", fill="y")

        # Evento <<TreeviewSelect>>: al seleccionar una fila, carga el usuario en el formulario.
        self.tabla_usuarios.bind("<<TreeviewSelect>>", self.al_seleccionar_usuario)

        self.refrescar_usuarios()

    def al_seleccionar_usuario(self, evento=None) -> None:
        """Callback del evento <<TreeviewSelect>>: obtiene el identificador
        de la fila seleccionada y solicita el usuario completo a
        RestauranteServicio (la tabla no guarda datos sensibles)."""
        seleccion = self.tabla_usuarios.selection()
        if not seleccion:
            return

        valores = self.tabla_usuarios.item(seleccion[0], "values")
        identificacion = valores[0]
        usuario = self.servicio.buscar_usuario(identificacion)
        if usuario is None:
            return

        self.variable_identificacion_usuario.set(usuario.identificacion)
        self.variable_nombre_persona.set(usuario.nombre)
        self.variable_login_usuario.set(usuario.nombre_usuario)
        self.variable_contrasena_usuario.set(usuario.contrasena)
        self.variable_rol_usuario.set(usuario.rol)
        self.variable_mensaje_usuarios.set(f"Usuario '{usuario.identificacion}' cargado desde la tabla.")
        self.etiqueta_mensaje_usuarios.configure(foreground="black")

    def al_cambiar_rol(self, evento=None) -> None:
        """Callback del evento <<ComboboxSelected>> del Combobox de rol."""
        rol_seleccionado = self.variable_rol_usuario.get()
        self.variable_mensaje_usuarios.set(f"Rol seleccionado: {rol_seleccionado}")
        self.etiqueta_mensaje_usuarios.configure(foreground="black")

    def manejar_enter_usuario(self, evento=None) -> None:
        """Callback de <Return>: reutiliza registrar_usuario(), el mismo
        método que usa el botón "Registrar" mediante command=."""
        self.registrar_usuario()

    def manejar_escape_usuario(self, evento=None) -> None:
        """Callback de <Escape>: reutiliza limpiar_formulario_usuario()."""
        self.limpiar_formulario_usuario()

    def registrar_usuario(self) -> None:
        exitoso, mensaje = self.servicio.registrar_usuario(
            self.variable_identificacion_usuario.get(),
            self.variable_nombre_persona.get(),
            self.variable_login_usuario.get(),
            self.variable_contrasena_usuario.get(),
            self.variable_rol_usuario.get(),
        )
        self.variable_mensaje_usuarios.set(mensaje)
        self.etiqueta_mensaje_usuarios.configure(foreground="green" if exitoso else "red")
        if exitoso:
            self.refrescar_usuarios()
            self.limpiar_formulario_usuario()

    def actualizar_usuario(self) -> None:
        exitoso, mensaje = self.servicio.actualizar_usuario(
            self.variable_identificacion_usuario.get(),
            self.variable_nombre_persona.get(),
            self.variable_login_usuario.get(),
            self.variable_contrasena_usuario.get(),
            self.variable_rol_usuario.get(),
        )
        self.variable_mensaje_usuarios.set(mensaje)
        self.etiqueta_mensaje_usuarios.configure(foreground="green" if exitoso else "red")
        if exitoso:
            self.refrescar_usuarios()

    def eliminar_usuario(self) -> None:
        identificacion = self.variable_identificacion_usuario.get().strip()

        if not identificacion:
            self.variable_mensaje_usuarios.set("Seleccione o escriba la identificación del usuario a eliminar.")
            self.etiqueta_mensaje_usuarios.configure(foreground="red")
            return

        confirmar = messagebox.askyesno(
            "Confirmar eliminación",
            f"¿Desea eliminar al usuario con identificación '{identificacion}'?",
        )
        if not confirmar:
            return

        exitoso, mensaje = self.servicio.eliminar_usuario(identificacion, self.usuario_actual.identificacion)
        self.variable_mensaje_usuarios.set(mensaje)
        self.etiqueta_mensaje_usuarios.configure(foreground="green" if exitoso else "red")
        if exitoso:
            self.refrescar_usuarios()
            self.limpiar_formulario_usuario()

    def limpiar_formulario_usuario(self) -> None:
        self.variable_identificacion_usuario.set("")
        self.variable_nombre_persona.set("")
        self.variable_login_usuario.set("")
        self.variable_contrasena_usuario.set("")
        self.variable_rol_usuario.set("")
        self.variable_mensaje_usuarios.set("")
        if self.tabla_usuarios is not None and self.tabla_usuarios.selection():
            self.tabla_usuarios.selection_remove(self.tabla_usuarios.selection())

    def refrescar_usuarios(self) -> None:
        if self.tabla_usuarios is None:
            return
        for fila in self.tabla_usuarios.get_children():
            self.tabla_usuarios.delete(fila)
        for usuario in self.servicio.listar_usuarios():
            self.tabla_usuarios.insert(
                "", tk.END,
                values=(usuario.identificacion, usuario.nombre, usuario.nombre_usuario, usuario.rol),
            )
        self.refrescar_combos_venta()

    # ------------------------------------------------------------------
    # Sección Ventas (desarrollada en la Semana 15)
    # ------------------------------------------------------------------
    def __construir_seccion_ventas(self) -> None:
        marco_formulario = ttk.LabelFrame(self.pestana_ventas, text="Registrar venta", padding=10)
        marco_formulario.pack(fill="x")

        ttk.Label(marco_formulario, text="Usuario:").grid(row=0, column=0, sticky="w", padx=5, pady=6)
        self.combo_usuario_venta = ttk.Combobox(
            marco_formulario, textvariable=self.variable_usuario_venta, state="readonly", width=35
        )
        self.combo_usuario_venta.grid(row=0, column=1, padx=5, pady=6)

        ttk.Label(marco_formulario, text="Producto:").grid(row=1, column=0, sticky="w", padx=5, pady=6)
        self.combo_producto_venta = ttk.Combobox(
            marco_formulario, textvariable=self.variable_producto_venta, state="readonly", width=35
        )
        self.combo_producto_venta.grid(row=1, column=1, padx=5, pady=6)

        ttk.Button(
            marco_formulario, text="Registrar venta", command=self.procesar_registro_venta
        ).grid(row=2, column=0, columnspan=2, pady=10)

        self.etiqueta_mensaje_venta = ttk.Label(marco_formulario, textvariable=self.variable_mensaje_venta)
        self.etiqueta_mensaje_venta.grid(row=3, column=0, columnspan=2, sticky="w", padx=5)

        marco_tabla = ttk.LabelFrame(self.pestana_ventas, text="Ventas registradas", padding=10)
        marco_tabla.pack(fill="both", expand=True, pady=(10, 0))

        columnas = ("usuario", "producto", "fecha")
        self.tabla_ventas = ttk.Treeview(marco_tabla, columns=columnas, show="headings", height=8)
        for columna, titulo, ancho in (
            ("usuario", "Usuario", 220),
            ("producto", "Producto", 250),
            ("fecha", "Fecha", 150),
        ):
            self.tabla_ventas.heading(columna, text=titulo)
            self.tabla_ventas.column(columna, width=ancho, anchor="w")

        self.tabla_ventas.pack(fill="both", expand=True)

    def procesar_registro_venta(self) -> None:
        clave_usuario = self.variable_usuario_venta.get()
        clave_producto = self.variable_producto_venta.get()

        identificacion_usuario = self.mapa_usuarios_venta.get(clave_usuario, "")
        codigo_producto = self.mapa_productos_venta.get(clave_producto, "")

        exitoso, mensaje = self.servicio.registrar_venta(identificacion_usuario, codigo_producto)

        self.variable_mensaje_venta.set(mensaje)
        self.etiqueta_mensaje_venta.configure(foreground="green" if exitoso else "red")

        if exitoso:
            self.refrescar_ventas()
            self.variable_usuario_venta.set("")
            self.variable_producto_venta.set("")

    def refrescar_ventas(self) -> None:
        for fila in self.tabla_ventas.get_children():
            self.tabla_ventas.delete(fila)

        mapa_nombres_usuario = {u.identificacion: u.nombre for u in self.servicio.listar_usuarios()}
        mapa_nombres_producto = {p.codigo: p.nombre for p in self.servicio.listar_productos()}

        for venta in self.servicio.listar_ventas():
            nombre_usuario = mapa_nombres_usuario.get(venta.usuario_id, venta.usuario_id)
            nombre_producto = mapa_nombres_producto.get(venta.producto_codigo, venta.producto_codigo)
            self.tabla_ventas.insert("", tk.END, values=(nombre_usuario, nombre_producto, venta.fecha))

    def refrescar_combos_venta(self) -> None:
        self.mapa_usuarios_venta = {
            f"{u.identificacion} - {u.nombre}": u.identificacion for u in self.servicio.listar_usuarios()
        }
        self.mapa_productos_venta = {
            f"{p.codigo} - {p.nombre}": p.codigo for p in self.servicio.listar_productos()
        }
        self.combo_usuario_venta.configure(values=list(self.mapa_usuarios_venta.keys()))
        self.combo_producto_venta.configure(values=list(self.mapa_productos_venta.keys()))

    # ------------------------------------------------------------------
    # Actualización general al ingresar
    # ------------------------------------------------------------------
    def actualizar_listas(self) -> None:
        self.limpiar_formulario()
        self.refrescar_productos()
        self.refrescar_usuarios()
        self.refrescar_ventas()
        self.refrescar_combos_venta()
