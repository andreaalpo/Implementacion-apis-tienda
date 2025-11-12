from flask import Flask 
from flasgger import Swagger
from flask_cors import CORS
from routes import Product
from config import config

app = Flask(__name__)
CORS(app)
# swagger = Swagger(app)  # inicializamos Swagger


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

# Configuración Swagger
app.config['SWAGGER'] = {
    'title': 'API Inventario - Tienda de barrio',
    'uiversion': 3,
}
swagger = Swagger(app)


if __name__ == '__main__':

    app.config.from_object(config['development'])
    

    # #blueprints
    # app.register_blueprint(Product.main, url_prefix='/api/productos')

    #manejador de error
    app.register_error_handler(404, page_not_found)
    app.run()