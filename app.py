"""
Aplicación CRUD para gestionar autos utilizando Flask y MongoDB.
Este archivo contiene la configuración principal de la aplicación.
"""

import os
from flask import Flask, render_template, request, redirect, url_for, flash
from pymongo import MongoClient
from bson import ObjectId
import yaml

def create_app(db_uri=None):
    """
    Función de fábrica para crear la aplicación Flask.
    Permite configurar diferentes conexiones de base de datos.
    """
    app = Flask(__name__)
    app.secret_key = 'your_secret_key_here'  # Necesario para flash messages

    # Configuración de la base de datos
    if not db_uri:
        # Si no se proporciona URI, intentar cargar desde secrets.yaml
            try:
                with open('secrets.yaml', 'r', encoding='utf-8') as file:
                    print("Archivo abierto correctamente")
                    secrets = yaml.safe_load(file)
                    db_uri = secrets['mongodb']['uri']
            except FileNotFoundError:
                print("No se encontró el archivo secrets.yaml")
                db_uri = 'mongodb://localhost:27017/'
            except KeyError as e:
                print("Error al acceder a la clave:", e)
                db_uri = 'mongodb://localhost:27017/'
            except Exception as e:
                print("Error inesperado:", e)
                db_uri = 'mongodb://localhost:27017/'

    # Conectar con MongoDB
    client = MongoClient(db_uri)
    
    # Usar base de datos de pruebas si es una conexión local
    if 'localhost' in db_uri:
        db = client.test_car_database
    else:
        db = client.car_database
    
    cars_collection = db.cars

    # Página principal que muestra la lista de autos
    @app.route('/')
    def index():
        """Renderiza la página principal con la lista de autos."""
        cars = cars_collection.find()
        return render_template('index.html', cars=cars)

    # Página de agregar auto
    @app.route('/add', methods=['GET', 'POST'])
    def add_car():
        """Permite agregar un nuevo auto a la base de datos."""
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
            flash('Auto agregado exitosamente', 'success')
            return redirect(url_for('index'))
        return render_template('add_car.html')

    # Página de editar auto
    @app.route('/edit/<car_id>', methods=['GET', 'POST'])
    def edit_car(car_id):
        """Permite editar los datos de un auto existente."""
        try:
            car = cars_collection.find_one({'_id': ObjectId(car_id)})
            
            if not car:
                flash('Auto no encontrado', 'danger')
                return redirect(url_for('index'))

            if request.method == 'POST':
                brand = request.form['brand']
                model = request.form['model']
                year = request.form['year']
                price = request.form['price']
                fuel_type = request.form['fuel_type']
                mileage = request.form['mileage']

                # Actualizar el auto en la base de datos
                cars_collection.update_one(
                    {'_id': ObjectId(car_id)},
                    {'$set': {
                        'brand': brand, 
                        'model': model, 
                        'year': year,
                        'price': price,
                        'fuel_type': fuel_type,
                        'mileage': mileage
                    }}
                )
                flash('Auto actualizado exitosamente', 'success')
                return redirect(url_for('index'))
            return render_template('edit_car.html', car=car)
        except Exception as e:
            flash(f'Error al editar el auto: {str(e)}', 'danger')
            return redirect(url_for('index'))

    # Página de eliminar auto
    @app.route('/delete/<car_id>', methods=['GET'])
    def delete_car(car_id):
        """Elimina un auto de la base de datos."""
        try:
            result = cars_collection.delete_one({'_id': ObjectId(car_id)})
            
            if result.deleted_count == 0:
                flash('Auto no encontrado', 'danger')
            else:
                flash('Auto eliminado exitosamente', 'success')
            
            return redirect(url_for('index'))
        except Exception as e:
            flash(f'Error al eliminar el auto: {str(e)}', 'danger')
            return redirect(url_for('index'))

    return app, cars_collection

# Crear la aplicación para ejecución normal
app, cars_collection = create_app()

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
