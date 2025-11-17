from flask import Blueprint, request, jsonify
#models
from models.Categoriamodel import CategoriaModel

#entities
from models.entities.Categoria import Categoria
from flask_jwt_extended import jwt_required, get_jwt_identity


main = Blueprint('category_blueprint', __name__)

@main.route('/', methods=['GET'])
def get_categories():
    """
    Obtener todas las categorias registradas en la base de datos.
    ---
    tags:
      - Categorias
    responses:
      200:
        description: Lista de categorias obtenida correctamente
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
                    example: "Despensa"
                  
      500:
        description: Error interno del servidor
        content:
          application/json:
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: "Error al obtener categorias"
    """

    try:
        categorias = CategoriaModel.get_categorias()
        return jsonify(categorias), 200
    except Exception as ex:
        return jsonify({'message': str(ex)}), 500

@main.route('/<id>', methods=['GET'])
def get_category(id):
    """
    Obtener una categoria por su ID.
    ---
    tags:
      - Categorias
    parameters:
      - name: id
        in: path
        required: true
        description: ID de la categoria a consultar
        schema:
          type: integer
          format: int64
          example: 1
    responses:
      200:
        description: Categoria encontrada correctamente
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
                  example: "Despensa"
                
      404:
        description: Categoria no encontrada
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
                  example: "Error al obtener categoria"
    """
    try:
        categoria = CategoriaModel.get_categoria(id)
        if categoria is not None:
            return jsonify(categoria), 200
        else:
            return jsonify({}), 404
    except Exception as ex:
        return jsonify({'message': str(ex)}), 500

   
@main.route('/add', methods=['POST'])
@jwt_required()
def add_category():
    """
    Agregar una nueva categoria
    ---
    tags:
      - Categorias
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
        description: Nombre de la categoria a agregar
        required: true
        schema:
          type: object
          required:
            - nombre
          properties:
            nombre:
              type: string
              example: "Despensa"
           
    responses:
      201:
        description: Categoria agregada correctamente
      500:
        description: Error interno del servidor
    """
    try:
        nombre = request.json['nombre']
       

        categoria = Categoria(None, nombre)
        CategoriaModel.add_categoria(categoria)
        return jsonify({'message': 'Categoria agregada correctamente'}), 201
    except Exception as ex:
        return jsonify({'message': str(ex)}), 500

   
@main.route('/delete/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_category(id):
    """
    Eliminar una categoria por su ID
    ---
    tags:
      - Categorias
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
        description: ID de la categoria a eliminar
    responses:
      200:
        description: Categoria eliminada correctamente
        examples:
          application/json: {"message": "Categoria eliminada correctamente"}
      404:
        description: Categoria no encontrada
        examples:
          application/json: {"message": "Ningúna categoria eliminada"}
      500:
        description: Error interno del servidor
        examples:
          application/json: {"message": "Error al eliminar la categoria"}
    """
    try:
        # Verificar si la categoria tiene productos asociados
        if CategoriaModel.tiene_productos(id):
            return jsonify({'message': 'No se puede eliminar la categoria porque tiene productos asociados'}), 400
        
        affected_rows = CategoriaModel.delete_categoria(id)
        if affected_rows > 0:
            return jsonify({'message': 'Categoria eliminada correctamente'}), 200
        else:
            return jsonify({'message': 'Ningúna categoria eliminada'}), 404
    except Exception as ex:
        return jsonify({'message': str(ex)}), 500


@main.route('/update/<id>', methods=['PUT'])
@jwt_required()
def update_category(id):
    """
    Actualizar una categoria 
    ---
    tags:
      - Categorias
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
        description: ID de la categoria que se desea actualizar
      - in: body
        name: body
        description: Campos de categoria que va a actualizar 
        required: true
        schema:
          type: object
          properties:
            nombre:
              type: string
              example: "Despensa"
           
    responses:
      200:
        description: Categoria actualizada correctamente
        examples:
          application/json: {"message": "Categoria actualizada correctamente"}
      404:
        description: Ningúna categoria actualizada (ID no encontrado)
        examples:
          application/json: {"message": "Ninguna categoria actualizada"}
      500:
        description: Error interno del servidor
        examples:
          application/json: {"message": "Error al actualizar la categoria"}
    """
    try:
        data = request.json  # datos recibidos del body
        categoria = CategoriaModel.get_categoria(id)

        if categoria is None:
            return jsonify({'message': 'Categoria no encontrada'}), 404

        # Actualiza solo los campos enviados en el JSON
        nombre = data.get('nombre', categoria['nombre'])
        

        categoria_actualizada = Categoria(id, nombre)
        affected_rows = CategoriaModel.update_categoria(categoria_actualizada)

        if affected_rows == 1:
            return jsonify({'message': 'Categoria actualizada correctamente'}), 200
        else:
            return jsonify({'message': 'Ninguna categoria actualizada'}), 404

    except Exception as ex:
        return jsonify({'message': str(ex)}), 500







