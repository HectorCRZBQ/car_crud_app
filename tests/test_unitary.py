"""
Pruebas unitarias para la aplicación CRUD de autos.
Este archivo utiliza pytest para verificar que las funciones
del CRUD de autos interactúan correctamente con la base de datos simulada.
"""
from bson import ObjectId
from app import app, cars_collection

def test_index_page(mocker):
    """
    Verifica que la página principal renderiza correctamente los datos.
    """
    # Mock the find method of cars_collection
    mock_find = mocker.patch.object(cars_collection, 'find')
    mock_find.return_value = [{'brand': 'Toyota', 'model': 'Corolla', 'year': 2020}]
    
    # Create a test client
    with app.test_client() as client:
        # Send a GET request to the index page
        response = client.get('/')
        
        # Assert the response status code and content
        assert response.status_code == 200
        assert b'Toyota' in response.data
    
    # Mensaje de éxito al pasar la prueba
    print("test_index_page: Página principal renderiza correctamente.")

def test_add_car(mocker):
    """
    Verifica que agregar un auto llama correctamente a la base de datos.
    """
    # Mock the insert_one method of cars_collection
    mock_insert_one = mocker.patch.object(cars_collection, 'insert_one')
    
    # Create a test client
    with app.test_client() as client:
        # Send a POST request to add a car
        response = client.post('/add', data={
            'brand': 'Tesla', 'model': 'Model 3', 'year': '2021',
            'price': '45000', 'fuel_type': 'Electric', 'mileage': '10000'
        })
        
        # Assert the response status code and method call
        assert response.status_code == 302  # Redirección a la página principal
        mock_insert_one.assert_called_once_with({
            'brand': 'Tesla', 'model': 'Model 3', 'year': '2021',
            'price': '45000', 'fuel_type': 'Electric', 'mileage': '10000'
        })
    
    # Mensaje de éxito al pasar la prueba
    print("test_add_car: Auto agregado correctamente y se llama al método insert_one.")

def test_edit_car(mocker):
    """
    Verifica que modificar un auto actualiza correctamente la base de datos simulada.
    """
    # Create a mock ObjectId and a mock car to be returned by find_one
    car_id = ObjectId()
    mock_car = {
        '_id': car_id,
        'brand': 'Ford', 'model': 'Mustang', 'year': '2022',
        'price': '60000', 'fuel_type': 'Gasoline', 'mileage': '5000'
    }
    
    # Mock the find_one method to return the mock car when trying to edit
    mock_find_one = mocker.patch.object(cars_collection, 'find_one', return_value=mock_car)
    
    # Mock the update_one method of cars_collection
    mock_update_one = mocker.patch.object(cars_collection, 'update_one')
    
    # Create a test client
    with app.test_client() as client:
        # Send a POST request to edit a car
        response = client.post(f'/edit/{car_id}', data={
            'brand': 'Ford', 'model': 'Mustang', 'year': '2022',
            'price': '60000', 'fuel_type': 'Gasoline', 'mileage': '5000'
        })
        
        # Assert the response status code and method call
        assert response.status_code == 302  # Redirección a la página principal
        mock_find_one.assert_called_once_with({'_id': car_id})
        mock_update_one.assert_called_once_with(
            {'_id': car_id},
            {'$set': {
                'brand': 'Ford', 'model': 'Mustang', 'year': '2022',
                'price': '60000', 'fuel_type': 'Gasoline', 'mileage': '5000'
            }}
        )
    
    # Mensaje de éxito al pasar la prueba
    print("test_edit_car: Auto editado correctamente y la base de datos simulada se actualiza.")

def test_delete_car(mocker):
    """
    Verifica que eliminar un auto llama al método de eliminación correctamente.
    """
    # Create a mock ObjectId
    car_id = ObjectId()
    
    # Mock the delete_one method of cars_collection
    mock_delete_one = mocker.patch.object(cars_collection, 'delete_one')
    
    # Create a test client
    with app.test_client() as client:
        # Send a GET request to delete a car
        response = client.get(f'/delete/{car_id}')
        
        # Assert the response status code and method call
        assert response.status_code == 302  # Redirección a la página principal
        mock_delete_one.assert_called_once_with({'_id': car_id})
    
    # Mensaje de éxito al pasar la prueba
    print("test_delete_car: Auto eliminado correctamente y el método delete_one fue llamado.")
