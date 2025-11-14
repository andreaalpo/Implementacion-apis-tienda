from database.db import get_db_connection
from .entities.Usuario import Usuario
from werkzeug.security import generate_password_hash, check_password_hash

class UsuarioModel:

    @classmethod
    def add_usuario(self, usuario):
        try:
            connection = get_db_connection()
            with connection.cursor() as cursor:
                hashed = generate_password_hash(usuario.password)  # guarda hash
                cursor.execute(
                    "INSERT INTO usuarios (nombre, email, password) VALUES (%s, %s, %s)",
                    (usuario.nombre, usuario.email, hashed)
                )
                connection.commit()
                affected = cursor.rowcount
            connection.close()
            return affected
        except Exception as ex:
            raise ex

    @classmethod
    def get_by_email(self, email):
        try:
            connection = get_db_connection()
            with connection.cursor() as cursor:
                cursor.execute("SELECT id, nombre, email, password FROM usuarios WHERE email = %s", (email,))
                row = cursor.fetchone()
            connection.close()
            if row:
                u = Usuario(id=row[0], nombre=row[1], email=row[2], password=row[3])
                return u
            return None
        except Exception as ex:
            raise ex

    @classmethod
    def get_usuario(self, id):
        try:
            connection = get_db_connection()
            with connection.cursor() as cursor:
                cursor.execute("SELECT id, nombre, email FROM usuarios WHERE id = %s", (id,))
                row = cursor.fetchone()
            connection.close()
            if row:
                u = Usuario(id=row[0], nombre=row[1], email=row[2])
                return u
            return None
        except Exception as ex:
            raise ex
