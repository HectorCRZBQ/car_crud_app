from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId #bson es una biblioteca de pymongo
import yaml

# Cargar credenciales desde secrets.yaml
with open('secrets.yaml', 'r') as file:
    secrets = yaml.safe_load(file)

# Conectar con MongoDB Atlas usando pymongo con soporte para SRV
client = MongoClient(secrets['mongodb']['uri'])
db = client.car_database
cars_collection = db.cars

app = Flask(__name__)

# Página principal que muestra la lista de autos
@app.route('/')
def index():
    cars = cars_collection.find()
    return render_template('index.html', cars=cars)

# Página de agregar auto
@app.route('/add', methods=['GET', 'POST'])
def add_car():
    if request.method == 'POST':
        brand = request.form['brand']
        model = request.form['model']
        year = request.form['year']
        price = request.form['price']
        fuel_type = request.form['fuel_type']
        mileage = request.form['mileage']
        
        # Insertar el nuevo auto en la base de datos
        cars_collection.insert_one({
            'brand': brand,
            'model': model,
            'year': year,
            'price': price,
            'fuel_type': fuel_type,
            'mileage': mileage
        })
        return redirect(url_for('index'))
    return render_template('add_car.html')

# Página de editar auto
@app.route('/edit/<car_id>', methods=['GET', 'POST'])
def edit_car(car_id):
    car = cars_collection.find_one({'_id': ObjectId(car_id)})  # Convertir car_id a ObjectId
    if request.method == 'POST':
        brand = request.form['brand']
        model = request.form['model']
        year = request.form['year']
        price = request.form['price']
        fuel_type = request.form['fuel_type']
        mileage = request.form['mileage']
        
        # Actualizar el auto en la base de datos
        cars_collection.update_one(
            {'_id': ObjectId(car_id)},  # Convertir car_id a ObjectId
            {'$set': {'brand': brand, 'model': model, 'year': year, 'price': price, 'fuel_type': fuel_type, 'mileage': mileage}}
        )
        return redirect(url_for('index'))
    return render_template('edit_car.html', car=car)

# Página de eliminar auto
@app.route('/delete/<car_id>', methods=['GET'])
def delete_car(car_id):
    # Convertir car_id a ObjectId antes de la eliminación
    cars_collection.delete_one({'_id': ObjectId(car_id)})  # Convertir car_id a ObjectId
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
