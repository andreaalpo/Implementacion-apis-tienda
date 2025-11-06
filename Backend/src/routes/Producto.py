from flask import Blueprint

main = Blueprint('producto_blueprint', __name__)


@main.route('/')
def home():
    return "Hello, World!"



@main.route('/create-product', methods=['GET', 'POST'])
def create():
    return "Create Page"

@main.route('/read')
def read():
    return "Read Page"

@main.route('/update')
def update():
    return "Update Page"

@main.route('/delete')
def delete():
    return "Delete Page"


@main.route('/read/<int:item_id>')
def read_item(item_id):
    return f"Estas viendo el producto con id {item_id}"