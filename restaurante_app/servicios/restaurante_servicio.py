from datetime import datetime
from typing import List, Optional, Tuple

from modelos.producto import Producto
from modelos.usuario import Usuario
from modelos.venta import Venta
from servicios.archivo_servicio import ArchivoServicio


class RestauranteServicio:
    ROLES_VALIDOS: Tuple[str, str, str] = ("Administrador", "Empleado", "Cliente")

    def __init__(self) -> None:
        self.__archivo_servicio: ArchivoServicio = ArchivoServicio()
        self.__productos: List[Producto] = self.__archivo_servicio.cargar_productos()
        self.__usuarios: List[Usuario] = self.__archivo_servicio.cargar_usuarios()
        self.__ventas: List[Venta] = self.__archivo_servicio.cargar_ventas()

    def validar_acceso(self, nombre_usuario: str, contrasena: str) -> Optional[Usuario]:
        for usuario in self.__usuarios:
            if usuario.nombre_usuario == nombre_usuario and usuario.contrasena == contrasena:
                return usuario
        return None

    def listar_usuarios(self) -> List[Usuario]:
        return list(self.__usuarios)

    def buscar_usuario(self, identificacion: str) -> Optional[Usuario]:
        identificacion_limpia = identificacion.strip()
        for usuario in self.__usuarios:
            if usuario.identificacion == identificacion_limpia:
                return usuario
        return None

    def es_administrador(self, usuario: Usuario) -> bool:
        return usuario.rol == "Administrador"

    def registrar_usuario(self, identificacion: str, nombre: str, nombre_usuario: str,
                          contrasena: str, rol: str) -> Tuple[bool, str]:
        valido, mensaje = self.__validar_datos_usuario(identificacion, nombre, nombre_usuario, contrasena, rol)
        if not valido:
            return False, mensaje

        if self.buscar_usuario(identificacion) is not None:
            return False, f"Ya existe un usuario con la identificación '{identificacion.strip()}'."

        if self.__existe_nombre_usuario(nombre_usuario, None):
            return False, f"Ya existe un usuario con el nombre de usuario '{nombre_usuario.strip()}'."

        usuario = Usuario(
            identificacion.strip(), nombre.strip(), nombre_usuario.strip(),
            contrasena.strip(), rol.strip()
        )
        self.__usuarios.append(usuario)
        self.__archivo_servicio.guardar_usuarios(self.__usuarios)
        return True, f"Usuario '{usuario.nombre}' registrado correctamente."

    def actualizar_usuario(self, identificacion: str, nombre: str, nombre_usuario: str,
                           contrasena: str, rol: str) -> Tuple[bool, str]:
        valido, mensaje = self.__validar_datos_usuario(identificacion, nombre, nombre_usuario, contrasena, rol)
        if not valido:
            return False, mensaje

        usuario = self.buscar_usuario(identificacion)
        if usuario is None:
            return False, f"No existe un usuario con la identificación '{identificacion.strip()}'."

        if self.__existe_nombre_usuario(nombre_usuario, usuario.identificacion):
            return False, f"Ya existe otro usuario con el nombre de usuario '{nombre_usuario.strip()}'."

        usuario.nombre = nombre.strip()
        usuario.nombre_usuario = nombre_usuario.strip()
        usuario.contrasena = contrasena.strip()
        usuario.rol = rol.strip()
        self.__archivo_servicio.guardar_usuarios(self.__usuarios)
        return True, f"Usuario '{usuario.identificacion}' actualizado correctamente."

    def eliminar_usuario(self, identificacion: str, identificacion_actual: str) -> Tuple[bool, str]:
        if not identificacion.strip():
            return False, "Debe indicar la identificación del usuario."

        if identificacion.strip() == identificacion_actual.strip():
            return False, "No puede eliminar la cuenta con la que está autenticado actualmente."

        usuario = self.buscar_usuario(identificacion)
        if usuario is None:
            return False, f"No existe un usuario con la identificación '{identificacion.strip()}'."

        self.__usuarios.remove(usuario)
        self.__archivo_servicio.guardar_usuarios(self.__usuarios)
        return True, f"Usuario '{usuario.identificacion}' eliminado correctamente."

    def __existe_nombre_usuario(self, nombre_usuario: str, identificacion_excluida: Optional[str]) -> bool:
        nombre_usuario_limpio = nombre_usuario.strip()
        for usuario in self.__usuarios:
            if usuario.nombre_usuario == nombre_usuario_limpio and usuario.identificacion != identificacion_excluida:
                return True
        return False

    def __validar_datos_usuario(self, identificacion: str, nombre: str, nombre_usuario: str,
                                contrasena: str, rol: str) -> Tuple[bool, str]:
        if not identificacion.strip() or not nombre.strip() or not nombre_usuario.strip() or not contrasena.strip():
            return False, "Identificación, nombre, usuario y contraseña son obligatorios."

        if rol.strip() not in self.ROLES_VALIDOS:
            return False, "Debe seleccionar un rol válido (Administrador, Empleado o Cliente)."

        return True, ""

    def listar_productos(self) -> List[Producto]:
        return list(self.__productos)

    def buscar_producto(self, codigo: str) -> Optional[Producto]:
        codigo_limpio = codigo.strip()
        for producto in self.__productos:
            if producto.codigo == codigo_limpio:
                return producto
        return None

    def consultar_cantidad(self, codigo: str) -> Optional[int]:
        producto = self.buscar_producto(codigo)
        return producto.stock if producto is not None else None

    def registrar_producto(self, codigo: str, nombre: str, categoria: str,
                           precio_texto: str, stock_texto: str) -> Tuple[bool, str]:
        valido, mensaje, precio, stock = self.__validar_datos(
            codigo, nombre, categoria, precio_texto, stock_texto
        )
        if not valido:
            return False, mensaje

        if self.buscar_producto(codigo) is not None:
            return False, f"Ya existe un producto con el código '{codigo.strip()}'."

        producto = Producto(codigo.strip(), nombre.strip(), categoria.strip(), precio, stock)
        self.__productos.append(producto)
        self.__archivo_servicio.guardar_productos(self.__productos)
        return True, f"Producto '{producto.nombre}' registrado correctamente."

    def actualizar_producto(self, codigo: str, nombre: str, categoria: str,
                            precio_texto: str, stock_texto: str) -> Tuple[bool, str]:
        valido, mensaje, precio, stock = self.__validar_datos(
            codigo, nombre, categoria, precio_texto, stock_texto
        )
        if not valido:
            return False, mensaje

        producto = self.buscar_producto(codigo)
        if producto is None:
            return False, f"No existe un producto con el código '{codigo.strip()}'."

        producto.nombre = nombre.strip()
        producto.categoria = categoria.strip()
        producto.precio = precio
        producto.stock = stock
        self.__archivo_servicio.guardar_productos(self.__productos)
        return True, f"Producto '{producto.codigo}' actualizado correctamente."

    def eliminar_producto(self, codigo: str) -> Tuple[bool, str]:
        if not codigo.strip():
            return False, "Debe indicar el código del producto."

        producto = self.buscar_producto(codigo)
        if producto is None:
            return False, f"No existe un producto con el código '{codigo.strip()}'."

        self.__productos.remove(producto)
        self.__archivo_servicio.guardar_productos(self.__productos)
        return True, f"Producto '{producto.codigo}' eliminado correctamente."

    def listar_ventas(self) -> List[Venta]:
        return list(self.__ventas)

    def registrar_venta(self, identificacion_usuario: str, codigo_producto: str) -> Tuple[bool, str]:
        if not identificacion_usuario.strip() or not codigo_producto.strip():
            return False, "Debe seleccionar un usuario y un producto."

        usuario = self.buscar_usuario(identificacion_usuario)
        if usuario is None:
            return False, f"No existe un usuario con la identificación '{identificacion_usuario.strip()}'."

        producto = self.buscar_producto(codigo_producto)
        if producto is None:
            return False, f"No existe un producto con el código '{codigo_producto.strip()}'."

        fecha_actual: str = datetime.now().strftime("%Y-%m-%d %H:%M")
        venta = Venta(usuario.identificacion, producto.codigo, fecha_actual)
        self.__ventas.append(venta)
        self.__archivo_servicio.guardar_ventas(self.__ventas)

        return True, f"Venta registrada: {producto.nombre} para {usuario.nombre}."

    def __validar_datos(self, codigo: str, nombre: str, categoria: str,
                        precio_texto: str, stock_texto: str) -> Tuple[bool, str, float, int]:
        if not codigo.strip() or not nombre.strip() or not categoria.strip():
            return False, "Código, nombre y categoría son obligatorios.", 0.0, 0

        try:
            precio = float(precio_texto)
        except ValueError:
            return False, "El precio debe ser un valor numérico.", 0.0, 0

        if precio <= 0:
            return False, "El precio debe ser mayor a cero.", 0.0, 0

        try:
            stock = int(stock_texto)
        except ValueError:
            return False, "El stock debe ser un número entero.", 0.0, 0

        if stock < 0:
            return False, "El stock no puede ser negativo.", 0.0, 0

        return True, "", precio, stock
