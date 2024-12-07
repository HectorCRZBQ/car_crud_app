"""
Pruebas de rendimiento utilizando Locust para la aplicación CRUD de autos.
Este script simula usuarios que interactúan con la API.
"""

from locust import HttpUser, task, between, events
import os
import signal

class WebsiteUser(HttpUser):
    """
    Simula un usuario interactuando con la aplicación web.
    """
    wait_time = between(1, 5)
    host = "http://localhost:5000"  # Cambia esto por la URL de tu servidor

    @task
    def index(self):
        """
        Realiza una solicitud GET a la página principal ('/').
        """
        self.client.get('/')

    @task
    def add_car(self):
        """
        Realiza una solicitud POST para agregar un nuevo auto.
        """
        self.client.post('/add', data={
            'brand': 'Tesla', 'model': 'Model S', 'year': '2022',
            'price': '80000', 'fuel_type': 'Electric', 'mileage': '5000'
        })

    @task
    def delete_car(self):
        """
        Realiza una solicitud GET para eliminar un auto.
        Utiliza un ID ficticio para propósitos de prueba.
        """
        self.client.get('/delete/60d5f77c7d81f2d9dbcd3a5d')  # ID ficticio

    @staticmethod
    def close_port():
        """
        Cierra el puerto del servidor de Locust (8089).
        Esta función intenta detener el proceso que está utilizando el puerto.
        """
        try:
            # Identifica los procesos usando el puerto 8089
            processes = os.popen("lsof -t -i :8089").read().strip()
            if processes:
                # Si hay varios procesos, se separan por saltos de línea
                for pid in processes.splitlines():
                    os.kill(int(pid), signal.SIGTERM)  # Matar el proceso
                print("Puerto 8089 cerrado correctamente.")
        except Exception as e:
            print(f"Error al intentar cerrar el puerto: {e}")

# Registrar el evento para cerrar el puerto cuando la prueba termine
@events.test_stop.add_listener
def on_test_stop(*args, **kwargs):
    WebsiteUser.close_port()
