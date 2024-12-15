import pytest
from app import create_app
from bson import ObjectId

@pytest.fixture
def app_and_client():
    """Configura una aplicación de pruebas con cliente."""
    # Usar una base de datos local de MongoDB
    app, cars_collection = create_app('mongodb://localhost:27017/')
    app.config['TESTING'] = True
    
    with app.test_client() as client:
        with app.app_context():
            yield app, client, cars_collection

def test_crud_operations(app_and_client):
    """
    Prueba completa de las operaciones CRUD:
    1. Insertar un nuevo auto
    2. Verificar la inserción
    3. Editar el auto
    4. Verificar la edición
    5. Eliminar el auto
    6. Verificar la eliminación
    """
    app, client, cars_collection = app_and_client

    # Datos de prueba
    test_car_data = {
        'brand': 'Toyota',
        'model': 'Corolla',
        'year': '2022',
        'price': '25000',
        'fuel_type': 'Gasolina',
        'mileage': '15000'
    }

    # 1. Prueba de inserción
    response = client.post('/add', data=test_car_data, follow_redirects=True)
    assert response.status_code == 200

    # 2. Verificar que el auto fue insertado
    inserted_car = cars_collection.find_one({'brand': 'Toyota', 'model': 'Corolla'})
    assert inserted_car is not None
    car_id = str(inserted_car['_id'])

    # 3. Prueba de edición
    edit_car_data = {
        'brand': 'Toyota',
        'model': 'Corolla',
        'year': '2023',  # Cambio de año
        'price': '26000',  # Cambio de precio
        'fuel_type': 'Gasolina',
        'mileage': '16000'
    }
    response = client.post(f'/edit/{car_id}', data=edit_car_data, follow_redirects=True)
    assert response.status_code == 200

    # 4. Verificar que el auto fue editado
    edited_car = cars_collection.find_one({'_id': ObjectId(car_id)})
    assert edited_car['year'] == '2023'
    assert edited_car['price'] == '26000'

    # 5. Prueba de eliminación
    response = client.get(f'/delete/{car_id}', follow_redirects=True)
    assert response.status_code == 200

    # 6. Verificar que el auto fue eliminado
    deleted_car = cars_collection.find_one({'_id': ObjectId(car_id)})
    assert deleted_car is None

def test_invalid_car_operations(app_and_client):
    """
    Pruebas de casos de error:
    1. Intentar editar un auto no existente
    2. Intentar eliminar un auto no existente
    """
    app, client, cars_collection = app_and_client

    # ID de prueba que no existe
    fake_id = '60afe2f86a4a5c8a8ce5c000'

    # Intentar editar un auto no existente
    edit_car_data = {
        'brand': 'Toyota',
        'model': 'Corolla',
        'year': '2023',
        'price': '26000',
        'fuel_type': 'Gasolina',
        'mileage': '16000'
    }
    
    response = client.post(f'/edit/{fake_id}', data=edit_car_data, follow_redirects=True)
    assert response.status_code == 200  # Redirige al index con mensaje de error

    # Intentar eliminar un auto no existente
    response = client.get(f'/delete/{fake_id}', follow_redirects=True)
    assert response.status_code == 200  # Redirige al index con mensaje de error