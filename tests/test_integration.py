"""
Pruebas de integración para la aplicación CRUD de autos.
Este archivo utiliza unittest para verificar la interacción entre
la aplicación y la base de datos MongoDB.
"""

import unittest
import os
from pymongo import MongoClient
from app import app

class TestIntegration(unittest.TestCase):
    """
    Clase que contiene las pruebas de integración para la aplicación CRUD de autos.
    """

    @classmethod
    def setUpClass(cls):
        """
        Configura la conexión a la base de datos de prueba antes de ejecutar las pruebas.
        """
        # Obtener la URI de MongoDB desde las variables de entorno configuradas en GitHub Secrets
        mongo_uri = os.getenv("MONGODB_URI")
        
        # Conectar a MongoDB usando la URI remota
        cls.client = MongoClient(mongo_uri)
        cls.db = cls.client.get_database('car_database')  # Especifica el nombre de la base de datos
        cls.cars_collection = cls.db.cars
        cls.app = app.test_client()

    def setUp(self):
        """
        Limpia la base de datos antes de cada prueba.
        """
        self.cars_collection.delete_many({})

    def test_add_car(self):
        """
        Verifica que agregar un auto lo inserta correctamente en la base de datos.
        """
        with self.app as client:
            response = client.post('/add', data={
                'brand': 'Honda', 'model': 'Civic', 'year': '2019',
                'price': '20000', 'fuel_type': 'Gasoline', 'mileage': '30000'
            })
            self.assertEqual(response.status_code, 302)  # Redirección a la página principal
            car = self.cars_collection.find_one({'brand': 'Honda'})
            self.assertIsNotNone(car)
            self.assertEqual(car['model'], 'Civic')

    def test_edit_car(self):
        """
        Verifica que modificar un auto lo actualiza correctamente en la base de datos.
        """
        car_id = self.cars_collection.insert_one({
            'brand': 'Nissan', 'model': 'Altima', 'year': '2018',
            'price': '18000', 'fuel_type': 'Gasoline', 'mileage': '40000'
        }).inserted_id
        with self.app as client:
            response = client.post(f'/edit/{car_id}', data={
                'brand': 'Nissan', 'model': 'Altima', 'year': '2020',
                'price': '19000', 'fuel_type': 'Gasoline', 'mileage': '35000'
            })
            self.assertEqual(response.status_code, 302)
            car = self.cars_collection.find_one({'_id': car_id})
            self.assertEqual(car['year'], '2020')
            self.assertEqual(car['price'], '19000')

    def test_delete_car(self):
        """
        Verifica que eliminar un auto lo elimina correctamente de la base de datos.
        """
        car_id = self.cars_collection.insert_one({
            'brand': 'Ford', 'model': 'Fiesta', 'year': '2015',
            'price': '10000', 'fuel_type': 'Gasoline', 'mileage': '70000'
        }).inserted_id
        with self.app as client:
            response = client.get(f'/delete/{car_id}')
            self.assertEqual(response.status_code, 302)
            car = self.cars_collection.find_one({'_id': car_id})
            self.assertIsNone(car)

    @classmethod
    def tearDownClass(cls):
        """
        Limpia la base de datos de prueba y cierra la conexión al final de las pruebas.
        """
        cls.client.drop_database(cls.db.name)  # Elimina la base de datos de pruebas
        cls.client.close()

if __name__ == '__main__':
    unittest.main()
