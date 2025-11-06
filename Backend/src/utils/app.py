from flask import Flask,request 

from config import Config

from routes import Producto

app = Flask(__name__)


def page_not_found(e):
    return "La página que buscas no existe", 404




if __name__ == '__main__':
    app.config.from_object(Config['development'])

    #blueprints
    app.register_blueprint(Producto.main, url_prefix='/api/productos')

    #manejador de error
    app.register_error_handler(404, page_not_found)
    app.run(debug=True)