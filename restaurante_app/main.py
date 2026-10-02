import tkinter as tk

from modelos.usuario import Usuario
from servicios.restaurante_servicio import RestauranteServicio
from ui.login_view import LoginView
from ui.main_view import MainView


class Aplicacion:
    def __init__(self, raiz: tk.Tk) -> None:
        self.raiz: tk.Tk = raiz
        self.raiz.title("Restaurante App - JoelFood")
        self.raiz.geometry("820x600")
        self.raiz.minsize(760, 560)

        self.servicio: RestauranteServicio = RestauranteServicio()

        self.contenedor = tk.Frame(self.raiz)
        self.contenedor.pack(fill="both", expand=True)
        self.contenedor.grid_rowconfigure(0, weight=1)
        self.contenedor.grid_columnconfigure(0, weight=1)

        self.login_view = LoginView(self.contenedor, self.servicio, self.mostrar_main_view)
        self.main_view = MainView(self.contenedor, self.servicio, self.mostrar_login_view)

        for vista in (self.login_view, self.main_view):
            vista.grid(row=0, column=0, sticky="nsew")

        self.mostrar_login_view()

    def mostrar_login_view(self) -> None:
        self.login_view.limpiar_campos()
        self.login_view.tkraise()

    def mostrar_main_view(self, usuario: Usuario) -> None:
        self.main_view.establecer_usuario_actual(usuario)
        self.main_view.actualizar_listas()
        self.main_view.tkraise()


def main() -> None:
    raiz = tk.Tk()
    Aplicacion(raiz)
    raiz.mainloop()


if __name__ == "__main__":
    main()
