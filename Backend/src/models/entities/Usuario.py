class Usuario:
    def __init__(self, id=None, nombre=None, email=None, password=None):
        self.id = id
        self.nombre = nombre
        self.email = email
        self.password = password

    def to_JSON(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'email': self.email,
        }
