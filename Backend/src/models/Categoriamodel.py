from database.db import get_db_connection
from .entities.Categoria import Categoria

class CategoriaModel():
    @classmethod
    def get_categorias(self):
        try:
            connection = get_db_connection()
            categorias = []
            with connection.cursor() as cursor:
                cursor.execute("SELECT id, nombre FROM categorias ORDER BY id;")
                resultset = cursor.fetchall()
                
            for row in resultset:
                categoria = Categoria(row[0], row[1])
                categorias.append(categoria.to_JSON())
            cursor.close()
            connection.close()
            return categorias
        except Exception as ex:
            raise ex
        

    @classmethod
    def get_categoria(self,id):
        try:
            connection = get_db_connection()

            with connection.cursor() as cursor:
                cursor.execute("SELECT id, nombre FROM categorias WHERE id = %s;", (id,))
                row = cursor.fetchone()
                
                categoria = None
                if row != None:
                    categoria = Categoria(row[0], row[1])
                    categoria=categoria.to_JSON()

            cursor.close()
            connection.close()
            return categoria
        except Exception as ex:
            raise ex
        


        
    @classmethod
    def add_categoria(self,categoria):
        try:
            connection = get_db_connection()

            with connection.cursor() as cursor:
                cursor.execute("INSERT INTO categorias (nombre) VALUES (%s);", (categoria.nombre,))
                affected_rows = cursor.rowcount
                connection.commit()
                
            connection.close()
            return affected_rows
        except Exception as ex:
            raise ex
        
    @classmethod
    def tiene_productos(self, categoria_id):
        try:
            connection = get_db_connection()
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT COUNT(*) 
                    FROM productos 
                    WHERE categoria_id = %s;
                """, (categoria_id,))
                count = cursor.fetchone()[0]

            connection.close()
            return count > 0  # True si tiene productos
        except Exception as ex:
            raise ex

        
    @classmethod
    def delete_categoria(self,id):
        try:
            connection = get_db_connection()

            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM categorias WHERE id = %s;", (id,))
                affected_rows = cursor.rowcount
                connection.commit()
                
            connection.close()
            return affected_rows
        except Exception as ex:
            raise ex
        

    @classmethod
    def update_categoria(self,categoria):
        try:
            connection = get_db_connection()

            with connection.cursor() as cursor:
                cursor.execute("""
                    UPDATE categorias 
                    SET nombre = %s
                    WHERE id = %s
                """, (categoria.nombre, categoria.id))
                affected_rows = cursor.rowcount
                connection.commit()
                
            connection.close()
            return affected_rows
        except Exception as ex:
            raise ex