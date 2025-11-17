from database.db import get_db_connection
from .entities.Producto import Producto


class ProductoModel():
    @classmethod
    def get_productos(self):
        try:
            connection = get_db_connection()
            productos = []
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT p.id, p.nombre, p.marca, p.cantidad, p.precio, 
                           p.categoria_id, c.nombre AS categoria_nombre
                    FROM productos p
                    LEFT JOIN categorias c ON p.categoria_id = c.id
                    ORDER BY p.id;
                """)                
                resultset = cursor.fetchall()
                
            for row in resultset:
                producto = Producto(row[0], row[1], row[2], row[3], row[4], row[5], row[6])
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
                cursor.execute("""
                    SELECT p.id, p.nombre, p.marca, p.cantidad, p.precio,
                           p.categoria_id, c.nombre AS categoria_nombre
                    FROM productos p
                    LEFT JOIN categorias c ON p.categoria_id = c.id
                    WHERE p.id = %s;
                """, (id,))

                row = cursor.fetchone()
                
                producto = None
                if row != None:
                    producto = Producto(row[0], row[1], row[2], row[3], row[4], row[5], row[6])
                    producto=producto.to_JSON()

            cursor.close()
            connection.close()
            return producto
        except Exception as ex:
            raise ex
        
    
    @classmethod
    def productos_por_categoria(self, categoria_id):
        try:
            connection = get_db_connection()
            productos = []

            query = """
                SELECT 
                    p.id, 
                    p.nombre, 
                    p.marca, 
                    p.cantidad, 
                    p.precio, 
                    p.categoria_id,
                    c.nombre AS categoria_nombre
                FROM productos p
                LEFT JOIN categorias c 
                    ON p.categoria_id = c.id
                WHERE p.categoria_id = %s
                ORDER BY p.nombre;
            """

            with connection.cursor() as cursor:
                cursor.execute(query, (categoria_id,))
                rows = cursor.fetchall()

            for row in rows:
                producto = Producto(
                    row[0],  
                    row[1],  
                    row[2],  
                    row[3],  
                    row[4],  
                    row[5],  
                    row[6]   
                )
                productos.append(producto.to_JSON())

            connection.close()
            return productos

        except Exception as ex:
            raise ex
        

    @classmethod
    def buscar_por_nombre(self, texto):
        try:
            connection = get_db_connection()
            productos = []

            query = """
                SELECT 
                    p.id,
                    p.nombre,
                    p.marca,
                    p.cantidad,
                    p.precio,
                    p.categoria_id,
                    c.nombre AS categoria_nombre
                FROM productos p
                LEFT JOIN categorias c 
                    ON p.categoria_id = c.id
                WHERE LOWER(p.nombre) LIKE LOWER(%s)
                ORDER BY p.nombre;
            """

            pattern = f"%{texto}%"   

            with connection.cursor() as cursor:
                cursor.execute(query, (pattern,))
                rows = cursor.fetchall()

            for row in rows:
                producto = Producto(
                    row[0],  
                    row[1],  
                    row[2],  
                    row[3],  
                    row[4],  
                    row[5],  
                    row[6]   
                )
                productos.append(producto.to_JSON())

            connection.close()
            return productos

        except Exception as ex:
            raise ex




        
    @classmethod
    def add_producto(self,product):
        try:
            connection = get_db_connection()

            with connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO productos (nombre, marca, cantidad, precio, categoria_id)
                    VALUES (%s, %s, %s, %s, %s)
                """, (product.nombre, product.marca, product.cantidad, product.precio, product.categoria_id))
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
                cursor.execute("""
                    UPDATE productos 
                    SET nombre = %s, marca = %s, cantidad = %s, precio = %s, categoria_id = %s
                    WHERE id = %s
                """, (product.nombre, product.marca, product.cantidad, product.precio, product.categoria_id, product.id, ))
                affected_rows = cursor.rowcount
                connection.commit()
                
            connection.close()
            return affected_rows
        except Exception as ex:
            raise ex