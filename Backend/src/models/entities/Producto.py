class Producto():

    def __init__(self, id, nombre, marca, cantidad, precio,categoria_id=None, categoria_nombre=None):
        self.id = id
        self.nombre = nombre
        self.marca = marca
        self.cantidad = cantidad
        self.precio = precio
        self.categoria_id = categoria_id            
        self.categoria_nombre = categoria_nombre    


    def to_JSON(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'marca': self.marca,
            'cantidad': self.cantidad,
            'precio': self.precio,
            'categoria_id': self.categoria_id,
            'categoria_nombre': self.categoria_nombre  
        }
  