from database.db import get_db_connection
from .entities.Producto import Producto

class ProductoModel():
    @classmethod
    def get_productos(self):
        try:
            connection = get_db_connection()
            productos = []
            with connection.cursor() as cursor:
                cursor.execute("SELECT id, nombre, marca, cantidad, precio FROM productos")
                resultset = cursor.fetchall()
                
            for row in resultset:
                producto = Producto(row[0], row[1], row[2], row[3], row[4])
                productos.append(producto.to_JSON())
            cursor.close()
            connection.close()
            return productos
        except Exception as ex:
            raise ex
        

    @classmethod
    def get_producto(self,id):
        try:
            connection = get_db_connection()

            with connection.cursor() as cursor:
                cursor.execute("SELECT id, nombre, marca, cantidad, precio FROM productos WHERE id = %s", (id,))
                row = cursor.fetchone()
                
                producto = None
                if row != None:
                    producto = Producto(row[0], row[1], row[2], row[3], row[4])
                    producto=producto.to_JSON()

            cursor.close()
            connection.close()
            return producto
        except Exception as ex:
            raise ex
        
    @classmethod
    def add_producto(self,product):
        try:
            connection = get_db_connection()

            with connection.cursor() as cursor:
                cursor.execute("""INSERT INTO productos (nombre, marca, cantidad, precio) 
                                   VALUES (%s, %s, %s, %s)""", (product.nombre, product.marca, product.cantidad, product.precio))
                affected_rows = cursor.rowcount
                connection.commit()
                
            connection.close()
            return affected_rows
        except Exception as ex:
            raise ex
        
    @classmethod
    def delete_producto(self,id):
        try:
            connection = get_db_connection()

            with connection.cursor() as cursor:
                cursor.execute("""DELETE FROM productos WHERE id = %s""", (id,))
                affected_rows = cursor.rowcount
                connection.commit()
                
            connection.close()
            return affected_rows
        except Exception as ex:
            raise ex
        

    @classmethod
    def update_producto(self,product):
        try:
            connection = get_db_connection()

            with connection.cursor() as cursor:
                cursor.execute("""UPDATE productos SET nombre= %s, marca= %s, cantidad= %s, precio= %s 
                                   WHERE id=%s""", (product.nombre, product.marca, product.cantidad, product.precio, product.id))
                affected_rows = cursor.rowcount
                connection.commit()
                
            connection.close()
            return affected_rows
        except Exception as ex:
            raise ex