class Venta:
    def __init__(self, usuario_id: str, producto_codigo: str, fecha: str) -> None:
        self.usuario_id: str = usuario_id
        self.producto_codigo: str = producto_codigo
        self.fecha: str = fecha

    def mostrar_informacion(self) -> str:
        return f"Usuario: {self.usuario_id} | Producto: {self.producto_codigo} | Fecha: {self.fecha}"

    def convertir_a_diccionario(self) -> dict:
        return {
            "usuario_id": self.usuario_id,
            "producto_codigo": self.producto_codigo,
            "fecha": self.fecha,
        }

    @classmethod
    def crear_desde_diccionario(cls, datos: dict) -> "Venta":
        return cls(
            usuario_id=datos["usuario_id"],
            producto_codigo=datos["producto_codigo"],
            fecha=datos["fecha"],
        )
