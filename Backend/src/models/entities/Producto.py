class Producto():

    def __init__(self, id, nombre, marca, cantidad, precio):
        self.id = id
        self.nombre = nombre
        self.marca = marca
        self.cantidad = cantidad
        self.precio = precio

    def to_JSON(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'marca': self.marca,
            'cantidad': self.cantidad,
            'precio': self.precio
        }
  