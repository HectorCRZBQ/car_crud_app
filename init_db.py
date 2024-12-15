from pymongo import MongoClient

def init_test_db():
    """Inicializa la base de datos de pruebas local con la misma estructura."""
    client = MongoClient('mongodb://localhost:27017')  # Conexión a MongoDB local
    db = client.test_car_database  # Base de datos de pruebas local
    cars_collection = db.cars  # Collección de autos

    # Limpiar la colección 'cars' antes de las pruebas
    cars_collection.drop()  # Elimina la colección 'cars' si ya existe

    # Agregar algunos autos de prueba para las pruebas de integración
    test_cars = [
        {
            'brand': 'Toyota',
            'model': 'Corolla',
            'year': 2020,
            'price': 15000,
            'fuel_type': 'Gasolina',
            'mileage': 30000
        },
        {
            'brand': 'Honda',
            'model': 'Civic',
            'year': 2021,
            'price': 20000,
            'fuel_type': 'Gasolina',
            'mileage': 15000
        },
        {
            'brand': 'Ford',
            'model': 'Focus',
            'year': 2019,
            'price': 18000,
            'fuel_type': 'Diesel',
            'mileage': 25000
        }
    ]

    # Insertar autos de prueba en la base de datos local
    cars_collection.insert_many(test_cars)

    # Cerrar la conexión
    client.close()
