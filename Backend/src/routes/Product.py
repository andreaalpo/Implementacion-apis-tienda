from flask import Blueprint, request, jsonify
#models
from models.Productomodel import ProductoModel

#entities
from models.entities.Producto import Producto
from flask_jwt_extended import jwt_required, get_jwt_identity



main = Blueprint('product_blueprint', __name__)

@main.route('/', methods=['GET'])
def get_products():
    """
    Obtener todos los productos registrados en la base de datos.
    ---
    tags:
      - Productos
    responses:
      200:
        description: Lista de productos obtenida correctamente
        content:
          application/json:
            schema:
              type: array
              items:
                type: object
                properties:
                  id:
                    type: integer
                    format: int64
                    example: 1
                  nombre:
                    type: string
                    example: "Shampoo Herbal"
                  marca:
                    type: string
                    example: "Herbal Essences"
                  cantidad:
                    type: integer
                    example: 20
                  precio:
                    type: number
                    format: float
                    example: 15900
                  categoria:
                    type: string
                    example: "Cuidado Personal"
      500:
        description: Error interno del servidor
        content:
          application/json:
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: "Error al obtener productos"
    """

    try:
        productos = ProductoModel.get_productos()
        return jsonify(productos), 200
    except Exception as ex:
        return jsonify({'message': str(ex)}), 500

@main.route('/<id>', methods=['GET'])
def get_product(id):
    """
    Obtener un producto por su ID.
    ---
    tags:
      - Productos
    parameters:
      - name: id
        in: path
        required: true
        description: ID del producto a consultar
        schema:
          type: integer
          format: int64
          example: 1
    responses:
      200:
        description: Producto encontrado correctamente
        content:
          application/json:
            schema:
              type: object
              properties:
                id:
                  type: integer
                  example: 1
                nombre:
                  type: string
                  example: "Shampoo Herbal"
                marca:
                  type: string
                  example: "Herbal Essences"
                cantidad:
                  type: integer
                  example: 20
                precio:
                  type: number
                  format: float
                  example: 15900
                categoria:
                  type: string
                  example: "Cuidado Personal"
      404:
        description: Producto no encontrado
        content:
          application/json:
            schema:
              type: object
              example: {}
      500:
        description: Error interno del servidor
        content:
          application/json:
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: "Error al obtener producto"
    """
    try:
        producto = ProductoModel.get_producto(id)
        if producto is not None:
            return jsonify(producto), 200
        else:
            return jsonify({}), 404
    except Exception as ex:
        return jsonify({'message': str(ex)}), 500

   
@main.route('/add', methods=['POST'])
@jwt_required()
def add_product():
    """
    Agregar un nuevo producto
    ---
    tags:
      - Productos
    security:
      - BearerAuth: []

    parameters:
      - in: header
        name: Authorization
        required: true
        type: string
        description: "Token JWT. Formato: Bearer {token}"

      - in: body
        name: body
        description: Datos del producto a agregar
        required: true
        schema:
          type: object
          required:
            - nombre
            - marca
            - cantidad
            - precio
          properties:
            nombre:
              type: string
              example: "Crema hidratante"
            marca:
              type: string
              example: "Nivea"
            cantidad:
              type: integer
              example: 10
            precio:
              type: number
              format: float
              example: 25900
            categoria_id:
              type: integer
              example: 2
    responses:
      201:
        description: Producto agregado correctamente
      500:
        description: Error interno del servidor
    """
    try:
        current_user_id = get_jwt_identity()

        nombre = request.json['nombre']
        marca = request.json['marca']
        cantidad = request.json['cantidad']
        precio = request.json['precio']
        categoria_id = request.json['categoria_id'] 

        producto = Producto(None, nombre, marca, cantidad, precio, categoria_id)
        ProductoModel.add_producto(producto)
        return jsonify({'message': 'Producto agregado correctamente', 'usuario: ' : current_user_id}), 201
    except Exception as ex:
        return jsonify({'message': str(ex)}), 500

   
@main.route('/delete/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_product(id):
    """
    Eliminar un producto por su ID
    ---
    tags:
      - Productos
    security:
      - BearerAuth: []

    parameters:
      - in: header
        name: Authorization
        required: true
        type: string
        description: "Token JWT. Formato: Bearer {token}"

      - name: id
        in: path
        type: integer
        required: true
        description: ID del producto a eliminar
    responses:
      200:
        description: Producto eliminado correctamente
        examples:
          application/json: {"message": "Producto eliminado correctamente"}
      404:
        description: Producto no encontrado
        examples:
          application/json: {"message": "Ningún producto eliminado"}
      500:
        description: Error interno del servidor
        examples:
          application/json: {"message": "Error al eliminar el producto"}
    """
    try:
        affected_rows = ProductoModel.delete_producto(id)
        if affected_rows > 0:
            return jsonify({'message': 'Producto eliminado correctamente'}), 200
        else:
            return jsonify({'message': 'Ningún producto eliminado'}), 404
    except Exception as ex:
        return jsonify({'message': str(ex)}), 500


@main.route('/update/<id>', methods=['PUT'])
@jwt_required()
def update_product(id):
    """
    Actualizar un producto (permite actualizar solo algunos campos)
    ---
    tags:
      - Productos
    security:
      - BearerAuth: []

    parameters:
      - in: header
        name: Authorization
        required: true
        type: string
        description: "Token JWT. Formato: Bearer {token}"

      - name: id
        in: path
        type: integer
        required: true
        description: ID del producto que se desea actualizar
      - in: body
        name: body
        description: Campos del producto a actualizar (puede enviar uno o varios)
        required: true
        schema:
          type: object
          properties:
            nombre:
              type: string
              example: "Crema hidratante"
            marca:
              type: string
              example: "Nivea"
            cantidad:
              type: integer
              example: 5
            precio:
              type: number
              format: float
              example: 25900
            categoria_id:
              type: integer
              example: 2
    responses:
      200:
        description: Producto actualizado correctamente
        examples:
          application/json: {"message": "Producto actualizado correctamente"}
      404:
        description: Ningún producto actualizado (ID no encontrado)
        examples:
          application/json: {"message": "Ningun producto actualizado"}
      500:
        description: Error interno del servidor
        examples:
          application/json: {"message": "Error al actualizar el producto"}
    """
    try:
        data = request.json  # datos recibidos del body
        producto = ProductoModel.get_producto(id)

        if producto is None:
            return jsonify({'message': 'Producto no encontrado'}), 404

        # Actualiza solo los campos enviados en el JSON
        nombre = data.get('nombre', producto['nombre'])
        marca = data.get('marca', producto['marca'])
        cantidad = data.get('cantidad', producto['cantidad'])
        precio = data.get('precio', producto['precio'])
        categoria_id = data.get('categoria_id', producto['categoria_id'])

        producto_actualizado = Producto(id, nombre, marca, cantidad, precio, categoria_id)
        affected_rows = ProductoModel.update_producto(producto_actualizado)

        if affected_rows == 1:
            return jsonify({'message': 'Producto actualizado correctamente'}), 200
        else:
            return jsonify({'message': 'Ningun producto actualizado'}), 404

    except Exception as ex:
        return jsonify({'message': str(ex)}), 500
    


@main.route('/por-categoria/<int:categoria_id>', methods=['GET'])
def productos_por_categoria(categoria_id):
    """
    Obtener productos filtrados por categoría
    ---
    tags:
      - Filtrar por categoria
    parameters:
      - name: categoria_id
        in: path
        required: true
        description: ID de la categoría
        schema:
          type: integer
    responses:
      200:
        description: Lista de productos filtrados
      404:
        description: No hay productos en esta categoría
    """
    try:
        productos = ProductoModel.productos_por_categoria(categoria_id)

        if not productos:
            return jsonify({'message': 'No hay productos en esta categoría'}), 404
        
        return jsonify(productos), 200

    except Exception as ex:
        return jsonify({'message': str(ex)}), 500
    

@main.route('/buscar', methods=['GET'])
def buscar_producto():
    """
    Buscar productos por nombre (coincidencia parcial)
    ---
    tags:
      - Filtrar por nombre de producto
    parameters:
      - name: nombre
        in: query
        required: true
        description: Texto a buscar en el nombre del producto
        schema:
          type: string
          example: "shampoo"
    responses:
      200:
        description: Lista de productos encontrados
    """
    try:
        nombre = request.args.get('nombre', '')

        if not nombre.strip():
            return jsonify({'message': 'Debe enviar un texto para buscar'}), 400

        productos = ProductoModel.buscar_por_nombre(nombre)
        return jsonify(productos), 200

    except Exception as ex:
        return jsonify({'message': str(ex)}), 500









