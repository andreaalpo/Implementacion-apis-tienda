from flask import Flask 
from flasgger import Swagger
from flask_cors import CORS
from routes import Product
from config import config

app = Flask(__name__)
swagger = Swagger(app)  # inicializamos Swagger
CORS(app)
def page_not_found(e):
    return "La página que buscas no existe", 404




if __name__ == '__main__':

    app.config.from_object(config['development'])
    

    #blueprints
    app.register_blueprint(Product.main, url_prefix='/api/productos')

    #manejador de error
    app.register_error_handler(404, page_not_found)
    app.run()