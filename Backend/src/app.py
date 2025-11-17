from flask import Flask, request
from flasgger import Swagger
from flask_cors import CORS
from routes import Product
from routes import Categoria
from routes import User
from config import config
import os
from datetime import timedelta
from dotenv import load_dotenv
from flask_jwt_extended import JWTManager

app = Flask(__name__)
CORS(app)


def page_not_found(e):
    return "La página que buscas no existe", 404

@app.route('/')
def home():
    return {
        'message': 'Backend Flask funcionando correctamente 🚀',
        'swagger_docs': '/apidocs/'
    }

# Blueprints
app.register_blueprint(Product.main, url_prefix='/api/productos')
app.register_blueprint(Categoria.main, url_prefix='/api/categorias')
app.register_blueprint(User.main, url_prefix='/api/auth')

# Configuración Swagger
app.config['SWAGGER'] = {
    'title': 'API Inventario - Tienda de barrio',
    'uiversion': 3,
}

swagger_template = {
    "securityDefinitions": {
        "Bearer": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "description": "Pega tu token sin la palabra Bearer. Ejemplo: eyJhbGciOi..."
        }
    },
    "security": [
        {"Bearer": []}
    ]
}


swagger = Swagger(app, template=swagger_template)



# carga variables del .env
load_dotenv() 

app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "dev-secret-change-me")
expires_seconds = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRES", "3600"))
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(seconds=expires_seconds)

# inicializa el gestor JWT
jwt = JWTManager(app)

from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
@app.before_request
def add_bearer_prefix():
    auth = request.headers.get("Authorization")
    if auth and not auth.startswith("Bearer "):
        request.headers.environ["HTTP_AUTHORIZATION"] = "Bearer " + auth


if __name__ == '__main__':

    app.config.from_object(config['development'])
    

    #manejador de error
    app.register_error_handler(404, page_not_found)
    app.run()