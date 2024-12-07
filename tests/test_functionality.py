"""
Pruebas funcionales para la aplicación CRUD de autos.
Este archivo contiene pruebas que verifican las funcionalidades
de agregar, editar y eliminar autos en la base de datos.
"""

import unittest
from app import app
from pymongo import MongoClient
from bson.objectid import ObjectId
from init_db import init_test_db  # Asumimos que tienes esta función para inicializar la DB de pruebas

class TestFunctionality(unittest.TestCase):
    """
    Clase que contiene pruebas funcionales para las operaciones de agregar y editar autos.
    Estas pruebas aseguran que las funcionalidades principales de la aplicación funcionen correctamente.
    """

    @classmethod
    def setUpClass(cls):
        """Configuración inicial para las pruebas"""
        init_test_db()  # Inicializamos la base de datos de pruebas
        cls.client = MongoClient('mongodb://localhost:27017')  # Conexión a MongoDB local
        cls.db = cls.client.test_car_database  # Base de datos para pruebas
        cls.cars_collection = cls.db.cars  # Colección de autos
        cls.app = app.test_client()
    
    def setUp(self):
        """Limpiar la colección antes de cada prueba"""
        self.cars_collection.delete_many({})  # Limpiar la colección de autos antes de cada prueba

    # --- PRUEBAS DE AGREGAR UN AUTO ---

    def test_add_car_missing_brand(self):
        """Probar agregar un auto con 'brand' faltante"""
        response = self.app.post('/add', data={
            'brand': '', 'model': 'Corolla', 'year': '2020',
            'price': '20000', 'fuel_type': 'Gasoline', 'mileage': '15000'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)  # Debería retornar el formulario con errores
        print("Test: test_add_car_missing_brand PASSED with status code:", response.status_code)

    def test_add_car_missing_model(self):
        """Probar agregar un auto con 'model' faltante"""
        response = self.app.post('/add', data={
            'brand': 'Toyota', 'model': '', 'year': '2020',
            'price': '20000', 'fuel_type': 'Gasoline', 'mileage': '15000'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        print("Test: test_add_car_missing_model PASSED with status code:", response.status_code)

    def test_add_car_missing_year(self):
        """Probar agregar un auto con 'year' faltante"""
        response = self.app.post('/add', data={
            'brand': 'Toyota', 'model': 'Corolla', 'year': '',
            'price': '20000', 'fuel_type': 'Gasoline', 'mileage': '15000'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        print("Test: test_add_car_missing_year PASSED with status code:", response.status_code)

    def test_add_car_missing_price(self):
        """Probar agregar un auto con 'price' faltante"""
        response = self.app.post('/add', data={
            'brand': 'Toyota', 'model': 'Corolla', 'year': '2020',
            'price': '', 'fuel_type': 'Gasoline', 'mileage': '15000'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        print("Test: test_add_car_missing_price PASSED with status code:", response.status_code)

    def test_add_car_missing_fuel_type(self):
        """Probar agregar un auto con 'fuel_type' faltante"""
        response = self.app.post('/add', data={
            'brand': 'Toyota', 'model': 'Corolla', 'year': '2020',
            'price': '20000', 'fuel_type': '', 'mileage': '15000'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        print("Test: test_add_car_missing_fuel_type PASSED with status code:", response.status_code)

    def test_add_car_missing_mileage(self):
        """Probar agregar un auto con 'mileage' faltante"""
        response = self.app.post('/add', data={
            'brand': 'Toyota', 'model': 'Corolla', 'year': '2020',
            'price': '20000', 'fuel_type': 'Gasoline', 'mileage': ''
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        print("Test: test_add_car_missing_mileage PASSED with status code:", response.status_code)

    # --- PRUEBAS DE EDITAR UN AUTO ---

    def test_edit_car_missing_brand(self):
        """Probar editar un auto con 'brand' faltante"""
        car_id = self.cars_collection.insert_one({
            'brand': 'Toyota', 'model': 'Corolla', 'year': '2020',
            'price': '20000', 'fuel_type': 'Gasoline', 'mileage': '15000'
        }).inserted_id

        response = self.app.post(f'/edit/{car_id}', data={
            'brand': '', 'model': 'Corolla', 'year': '2020',
            'price': '20000', 'fuel_type': 'Gasoline', 'mileage': '15000'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        print("Test: test_edit_car_missing_brand PASSED with status code:", response.status_code)

    def test_edit_car_missing_model(self):
        """Probar editar un auto con 'model' faltante"""
        car_id = self.cars_collection.insert_one({
            'brand': 'Toyota', 'model': 'Corolla', 'year': '2020',
            'price': '20000', 'fuel_type': 'Gasoline', 'mileage': '15000'
        }).inserted_id

        response = self.app.post(f'/edit/{car_id}', data={
            'brand': 'Toyota', 'model': '', 'year': '2020',
            'price': '20000', 'fuel_type': 'Gasoline', 'mileage': '15000'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        print("Test: test_edit_car_missing_model PASSED with status code:", response.status_code)

    def test_edit_car_missing_year(self):
        """Probar editar un auto con 'year' faltante"""
        car_id = self.cars_collection.insert_one({
            'brand': 'Toyota', 'model': 'Corolla', 'year': '2020',
            'price': '20000', 'fuel_type': 'Gasoline', 'mileage': '15000'
        }).inserted_id

        response = self.app.post(f'/edit/{car_id}', data={
            'brand': 'Toyota', 'model': 'Corolla', 'year': '',
            'price': '20000', 'fuel_type': 'Gasoline', 'mileage': '15000'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        print("Test: test_edit_car_missing_year PASSED with status code:", response.status_code)

    def test_edit_car_missing_price(self):
        """Probar editar un auto con 'price' faltante"""
        car_id = self.cars_collection.insert_one({
            'brand': 'Toyota', 'model': 'Corolla', 'year': '2020',
            'price': '20000', 'fuel_type': 'Gasoline', 'mileage': '15000'
        }).inserted_id

        response = self.app.post(f'/edit/{car_id}', data={
            'brand': 'Toyota', 'model': 'Corolla', 'year': '2020',
            'price': '', 'fuel_type': 'Gasoline', 'mileage': '15000'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        print("Test: test_edit_car_missing_price PASSED with status code:", response.status_code)

    def test_edit_car_missing_fuel_type(self):
        """Probar editar un auto con 'fuel_type' faltante"""
        car_id = self.cars_collection.insert_one({
            'brand': 'Toyota', 'model': 'Corolla', 'year': '2020',
            'price': '20000', 'fuel_type': 'Gasoline', 'mileage': '15000'
        }).inserted_id

        response = self.app.post(f'/edit/{car_id}', data={
            'brand': 'Toyota', 'model': 'Corolla', 'year': '2020',
            'price': '20000', 'fuel_type': '', 'mileage': '15000'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        print("Test: test_edit_car_missing_fuel_type PASSED with status code:", response.status_code)

    def test_edit_car_missing_mileage(self):
        """Probar editar un auto con 'mileage' faltante"""
        car_id = self.cars_collection.insert_one({
            'brand': 'Toyota', 'model': 'Corolla', 'year': '2020',
            'price': '20000', 'fuel_type': 'Gasoline', 'mileage': '15000'
        }).inserted_id

        response = self.app.post(f'/edit/{car_id}', data={
            'brand': 'Toyota', 'model': 'Corolla', 'year': '2020',
            'price': '20000', 'fuel_type': 'Gasoline', 'mileage': ''
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        print("Test: test_edit_car_missing_mileage PASSED with status code:", response.status_code)

    # --- Limpiar la base de datos temporal después de las pruebas ---

    @classmethod
    def tearDownClass(cls):
        """Limpiar después de todas las pruebas eliminando la base de datos local"""
        if hasattr(cls, 'client'):
            # Listar todas las bases de datos
            db_names = cls.client.list_database_names()  # Obtenemos todas las bases de datos

            # Si tu base de datos de pruebas es la primera que aparece en la lista
            # o sabes el nombre, puedes acceder directamente a ella y eliminarla
            if 'test_car_database' in db_names:
                cls.client.drop_database('test_car_database')  # Eliminar la base de datos de pruebas

            # Si la base de datos no tiene un nombre fijo y quieres eliminar todas las bases de datos temporales
            for db_name in db_names:
                if db_name != 'admin' and db_name != 'local':  # No eliminar bases de datos internas de MongoDB
                    cls.client.drop_database(db_name)  # Eliminar otras bases de datos

            cls.client.close()  # Cierra la conexión al cliente MongoDB



if __name__ == '__main__':
    unittest.main()
