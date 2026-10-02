class Usuario:
    def __init__(self, identificacion: str, nombre: str, nombre_usuario: str,
                 contrasena: str, rol: str) -> None:
        self.identificacion: str = identificacion
        self.nombre: str = nombre
        self.nombre_usuario: str = nombre_usuario
        self.contrasena: str = contrasena
        self.rol: str = rol

    def mostrar_informacion(self) -> str:
        return (
            f"{self.identificacion} | {self.nombre} | Usuario: {self.nombre_usuario} "
            f"| Rol: {self.rol}"
        )

    def convertir_a_diccionario(self) -> dict:
        return {
            "identificacion": self.identificacion,
            "nombre": self.nombre,
            "nombre_usuario": self.nombre_usuario,
            "contrasena": self.contrasena,
            "rol": self.rol,
        }

    @classmethod
    def crear_desde_diccionario(cls, datos: dict) -> "Usuario":
        return cls(
            identificacion=datos["identificacion"],
            nombre=datos["nombre"],
            nombre_usuario=datos["nombre_usuario"],
            contrasena=datos["contrasena"],
            rol=datos["rol"],
        )
