from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

class Producto:
    def __init__(self, codigo, nombre, cantidad, fecha_vencimiento):
        self.codigo = codigo
        self.nombre = nombre
        self.cantidad = cantidad
        self.fecha_vencimiento = fecha_vencimiento

    def registrar_entrada(self, cantidad):
        self.cantidad += cantidad

    def registrar_salida(self, cantidad):
        if self.cantidad >= cantidad:
            self.cantidad -= cantidad
        else:
            raise ValueError("Cantidad insuficiente en inventario")


inventario = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/productos', methods=['GET'])
def listar_productos():
    productos = {codigo: vars(producto) for codigo, producto in inventario.items()}
    return jsonify(productos)

@app.route('/productos/<codigo>', methods=['GET'])
def obtener_producto(codigo):
    producto = inventario.get(codigo)
    if producto:
        return jsonify(vars(producto))
    else:
        return jsonify({'error': 'Producto no encontrado'}), 404

@app.route('/productos', methods=['POST'])
def agregar_producto():
    datos = request.json
    codigo = datos.get('codigo')
    if codigo in inventario:
        return jsonify({'error': 'El producto ya existe'}), 400
    
    nuevo_producto = Producto(
        codigo=codigo,
        nombre=datos.get('nombre'),
        cantidad=datos.get('cantidad'),
        fecha_vencimiento=datos.get('fecha_vencimiento')
    )
    inventario[codigo] = nuevo_producto
    return jsonify({'mensaje': 'Producto agregado exitosamente'}), 201

@app.route('/productos/<codigo>', methods=['PUT'])
def actualizar_producto(codigo):
    producto = inventario.get(codigo)
    if not producto:
        return jsonify({'error': 'Producto no encontrado'}), 404
    
    datos = request.json
    producto.nombre = datos.get('nombre', producto.nombre)
    producto.cantidad = datos.get('cantidad', producto.cantidad)
    producto.fecha_vencimiento = datos.get('fecha_vencimiento', producto.fecha_vencimiento)
    return jsonify({'mensaje': 'Producto actualizado exitosamente'})

@app.route('/productos/<codigo>', methods=['DELETE'])
def eliminar_producto(codigo):
    if codigo in inventario:
        del inventario[codigo]
        return jsonify({'mensaje': 'Producto eliminado exitosamente'})
    else:
        return jsonify({'error': 'Producto no encontrado'}), 404

if __name__ == '__main__':
    app.run(debug=True)
