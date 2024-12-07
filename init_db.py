from pymongo import MongoClient

def init_test_db():
    """Inicializa la base de datos de pruebas (sin definir la estructura)"""
    client = MongoClient('mongodb://localhost:27017')  # Conexión a MongoDB local
    db = client.test_car_database  # Base de datos de pruebas
    # Si es necesario, se puede limpiar la colección 'cars' antes de las pruebas
    db.cars.drop()  # Elimina la colección 'cars' si ya existe (esto es opcional)
    client.close()  # Cerramos la conexión
