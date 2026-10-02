import json
from pathlib import Path
from typing import List

from modelos.producto import Producto
from modelos.usuario import Usuario
from modelos.venta import Venta

CARPETA_DATOS: Path = Path(__file__).resolve().parent.parent / "datos"
RUTA_PRODUCTOS: Path = CARPETA_DATOS / "productos.json"
RUTA_USUARIOS: Path = CARPETA_DATOS / "usuarios.json"
RUTA_VENTAS: Path = CARPETA_DATOS / "ventas.json"


class ArchivoServicio:
    def cargar_productos(self) -> List[Producto]:
        registros = self.__leer_json(RUTA_PRODUCTOS)
        productos: List[Producto] = []
        for registro in registros:
            try:
                productos.append(Producto.crear_desde_diccionario(registro))
            except KeyError as error:
                print(f"Registro de producto incompleto, se omite: falta la clave {error}")
        return productos

    def cargar_usuarios(self) -> List[Usuario]:
        registros = self.__leer_json(RUTA_USUARIOS)
        usuarios: List[Usuario] = []
        for registro in registros:
            try:
                usuarios.append(Usuario.crear_desde_diccionario(registro))
            except KeyError as error:
                print(f"Registro de usuario incompleto, se omite: falta la clave {error}")
        return usuarios

    def cargar_ventas(self) -> List[Venta]:
        registros = self.__leer_json(RUTA_VENTAS)
        ventas: List[Venta] = []
        for registro in registros:
            try:
                ventas.append(Venta.crear_desde_diccionario(registro))
            except KeyError as error:
                print(f"Registro de venta incompleto, se omite: falta la clave {error}")
        return ventas

    def guardar_productos(self, productos: List[Producto]) -> None:
        registros = [producto.convertir_a_diccionario() for producto in productos]
        self.__escribir_json(RUTA_PRODUCTOS, registros)

    def guardar_usuarios(self, usuarios: List[Usuario]) -> None:
        registros = [usuario.convertir_a_diccionario() for usuario in usuarios]
        self.__escribir_json(RUTA_USUARIOS, registros)

    def guardar_ventas(self, ventas: List[Venta]) -> None:
        registros = [venta.convertir_a_diccionario() for venta in ventas]
        self.__escribir_json(RUTA_VENTAS, registros)

    def __leer_json(self, ruta: Path) -> list:
        try:
            with open(ruta, "r", encoding="utf-8") as archivo:
                return json.load(archivo)
        except FileNotFoundError:
            print(f"No se encontró el archivo {ruta.name}. Se usará una lista vacía.")
            return []
        except json.JSONDecodeError:
            print(f"El archivo {ruta.name} contiene datos inválidos. Se usará una lista vacía.")
            return []
        except PermissionError:
            print(f"No se tienen permisos para leer {ruta.name}. Se usará una lista vacía.")
            return []

    def __escribir_json(self, ruta: Path, registros: list) -> None:
        try:
            with open(ruta, "w", encoding="utf-8") as archivo:
                json.dump(registros, archivo, indent=4, ensure_ascii=False)
        except PermissionError:
            print(f"No se tienen permisos para escribir en {ruta.name}. Los cambios no se guardaron.")
