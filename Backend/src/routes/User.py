from flask import Blueprint, request, jsonify
from models.Usuariomodel import UsuarioModel
from models.entities.Usuario import Usuario
from werkzeug.security import check_password_hash
from flask_jwt_extended import create_access_token

main = Blueprint('auth_blueprint', __name__)


@main.route('/register', methods=['POST'])
def register():
    """
    Registrar usuario
    ---
    tags:
      - Auth
    parameters:
      - in: body
        name: body
        schema:
          type: object
          required: [nombre, email, password]
          properties:
            nombre:
              type: string
            email:
              type: string
            password:
              type: string
    responses:
      201:
        description: Usuario registrado
      400:
        description: Datos inválidos / email ya existe
    """
    data = request.get_json()
    nombre = data.get('nombre')
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'message': 'email y password son requeridos'}), 400

    existing = UsuarioModel.get_by_email(email)
    if existing:
        return jsonify({'message': 'Email ya registrado'}), 400

    usuario = Usuario(None, nombre, email, password)
    UsuarioModel.add_usuario(usuario)
    return jsonify({'message': 'Usuario registrado correctamente'}), 201


@main.route('/login', methods=['POST'])
def login():
    """
    Login usuario
    ---
    tags:
      - Auth
    parameters:
      - in: body
        name: body
        schema:
          type: object
          required: [email, password]
          properties:
            email:
              type: string
            password:
              type: string
    responses:
      200:
        description: Login exitoso (devuelve token)
    """
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = UsuarioModel.get_by_email(email)
    if not user or not check_password_hash(user.password, password):
        return jsonify({'message': 'Credenciales incorrectas'}), 401

    access_token = create_access_token(identity=str(user.id))
    return jsonify({'access_token': access_token, 'usuario': {'id': user.id, 'nombre': user.nombre, 'email': user.email}}), 200
