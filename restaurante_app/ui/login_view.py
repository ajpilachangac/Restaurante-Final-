import tkinter as tk
from pathlib import Path
from tkinter import ttk
from typing import Callable

from modelos.usuario import Usuario
from servicios.restaurante_servicio import RestauranteServicio

CARPETA_ASSETS: Path = Path(__file__).resolve().parent.parent / "assets"


class LoginView(ttk.Frame):
    def __init__(self, contenedor: tk.Widget, servicio: RestauranteServicio,
                 al_iniciar_sesion: Callable[[Usuario], None]) -> None:
        super().__init__(contenedor, padding=20)
        self.servicio: RestauranteServicio = servicio
        self.al_iniciar_sesion: Callable[[Usuario], None] = al_iniciar_sesion

        self.variable_usuario = tk.StringVar()
        self.variable_contrasena = tk.StringVar()
        self.variable_mensaje = tk.StringVar()

        marco_central = ttk.Frame(self)
        marco_central.place(relx=0.5, rely=0.5, anchor="center")

        try:
            self.logo = tk.PhotoImage(file=str(CARPETA_ASSETS / "logo.png"))
            ttk.Label(marco_central, image=self.logo).pack(pady=(0, 10))
        except tk.TclError:
            self.logo = None

        ttk.Label(
            marco_central, text="Restaurante JoelFood", font=("Arial", 18, "bold")
        ).pack(pady=(0, 5))
        ttk.Label(marco_central, text="Acceso al sistema").pack(pady=(0, 15))

        marco_credenciales = ttk.LabelFrame(marco_central, text="Credenciales", padding=15)
        marco_credenciales.pack()

        ttk.Label(marco_credenciales, text="Usuario:").grid(row=0, column=0, sticky="w", pady=5, padx=5)
        ttk.Entry(marco_credenciales, textvariable=self.variable_usuario, width=22).grid(
            row=0, column=1, pady=5, padx=5
        )

        ttk.Label(marco_credenciales, text="Contraseña:").grid(row=1, column=0, sticky="w", pady=5, padx=5)
        ttk.Entry(marco_credenciales, textvariable=self.variable_contrasena, show="*", width=22).grid(
            row=1, column=1, pady=5, padx=5
        )

        ttk.Button(marco_central, text="Ingresar", command=self.procesar_ingreso).pack(pady=15)

        self.etiqueta_mensaje = ttk.Label(marco_central, textvariable=self.variable_mensaje, foreground="red")
        self.etiqueta_mensaje.pack()

    def procesar_ingreso(self) -> None:
        nombre_usuario: str = self.variable_usuario.get().strip()
        contrasena: str = self.variable_contrasena.get().strip()

        if not nombre_usuario or not contrasena:
            self.variable_mensaje.set("Ingrese usuario y contraseña.")
            return

        usuario_valido = self.servicio.validar_acceso(nombre_usuario, contrasena)

        if usuario_valido is None:
            self.variable_mensaje.set("Credenciales incorrectas.")
            return

        self.variable_mensaje.set("")
        self.al_iniciar_sesion(usuario_valido)

    def limpiar_campos(self) -> None:
        self.variable_usuario.set("")
        self.variable_contrasena.set("")
        self.variable_mensaje.set("")
