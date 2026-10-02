class Producto:
    def __init__(self, codigo: str, nombre: str, categoria: str, precio: float, stock: int) -> None:
        self.codigo: str = codigo
        self.nombre: str = nombre
        self.categoria: str = categoria
        self.precio: float = precio
        self.stock: int = stock

    def mostrar_informacion(self) -> str:
        return (
            f"{self.codigo} | {self.nombre} | {self.categoria} "
            f"| ${self.precio:.2f} | Stock: {self.stock}"
        )

    @classmethod
    def crear_desde_diccionario(cls, datos: dict) -> "Producto":
        return cls(
            codigo=datos["codigo"],
            nombre=datos["nombre"],
            categoria=datos["categoria"],
            precio=datos["precio"],
            stock=datos["stock"],
        )

    def convertir_a_diccionario(self) -> dict:
        return {
            "codigo": self.codigo,
            "nombre": self.nombre,
            "categoria": self.categoria,
            "precio": self.precio,
            "stock": self.stock,
        }
