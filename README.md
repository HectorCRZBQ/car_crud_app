# CAR_CRUD_APP

### La idea del proyecto es implementar un ciclo CI/CD completo sobre una aplicación CRUD básica de gestión de inventario de vehículos.

Las fases a seguir van a ser:

1. Plan (Notion)
2. Code (Python)
3. Build (GithubActions)
4. Test (Pytest (Test generales) + Locust (Test de rendimiento) +  Trivy (Test de seguridad) )
5. Release (GithubActions / Git tagging)
6. Deploy (AWS / Google Cloud)
7. Operate (Terraform)
8. Monitor (Grafana o Prometheus (Back) y Google Analytics (Front))

## 1. Plan 

Planificación en **Notion**: https://www.notion.so/car_crud_app-14f7a0c76b9780d9af6ad93edb027a83?pvs=4

## 2. Code 
Se comienza por definir la estructura basica del proyecto:

 - **app.py** con las funcionalidades de CRUD de la aplicación.
 - Una carpeta **templates** donde declaramos las siguientes estructuras:
    - base.html -> estructura basica general.
    - index.html -> estructura para mostrar el contenido de la base de datos.
    - add_car.html -> estrutura interactiva para añadir un objeto a la base de datos.
    - edit_car.html -> estrutura interactiva para modificar un objeto existente de la base de datos.
 - Una carpeta **static** donde declaramos las siguientes estructuras:
    - base.html -> estilos generales de la estructura 
 - **requierements.txt** con todas las dependencias del proyecto hasta la fecha.
 - **prompts.md** memoria donde se redactan las interacciones con módelos de LLM.
 - **.tool-versions** definir herramientas y sus verisiones usadas en el proyecto para evitar problemas.
 - **.gitignore** decalara los archivos que no se deben incorporar al repositorio en los commits.
 - **secrets.yaml** con los credenciales y datos privados, que luego seran encriptados para evitar problemas.
 - **README.md** memoria descriptiva con los pasos, decisiones y avances realizados en el proyecto.
 - Una base de datos Atlas de MongoDB

Los campos que vamos a manejar para está aplicación son los siguientes:

- brand (marca)
- model (modelo)
- year (año)
- price (precio)
- fuel_type (tipo de combustible)
- mileage (kilometraje)


Una de las primeras acciones a realizar es crear el entorno virtual con los siguientes comandos:

```
python3 -m venv venv # Crear el entorno virtual

source venv/bin/activate # Activar el entorno virtual

pip install -r requirements.txt # Instalar los requisitos necesarios
```

Ejecutamos el comando para activar la aplicacíon flask con el comando:

```
python app.py
```
Accedemos al puerto http://127.0.0.1:5000/

## 3. Build

Se va a hacer uso de Github Actions para automatizar las siguientes fases que vamos a realizar.

Añadimos a la estructura de proyecto los siguientes elementos:
 - Creamos el directorio **.github/workflows** para guardar los el fujo de trabajo de GithubActions bajo el nombre de **pipeline.yaml**:
    - build: construcción de la aplicación.
    - test: ejecucción de los test correspondientes.
    - release: creación del etiquetado, creación de versiones y análisis de seguridad.
    - deploy: despliegue en la nube de AWS/Google Cloud con Terraform.
    - monitor: monitorización de la aplicación.

Dentro del código en la parte de **build** de GithubActions vamos a realizar los siguientes acciones:
 - Revisar el repositorio
 - Iniciar Python
 - Crear el entorno virtual, iniciarlo y descargar las dependencias


## 4. Test

Añadimos a la estructura de proyecto los siguientes elementos:
 - Creamos el directorio **tests** donde almacenamos los tests que vamos a realizar sobre la aplicación:
    - test_unitary.py -> pruebas de lógica de la aplicación usnado mocking simulando la base de datos.
    - test_integration.py -> pruebas de integración de elementos para garantizar la integridad de los objetos
    - test_functionality.py -> pruebas de funcionalidad de la aplicación con varios usuarios simulados
    - test_performance.py -> pruebas de rendimiento usado Locust 
    - test_quality.py -> evaluar la calidad del codigo html usando Pylint
    - test_security.sh -> pruebas de seguridad usando Trivy

1. En test_unitary.py evaluamos los siguientes elementos:
 - Añadir objetos en base de datos simulada
 - Editar objetos en base de datos simulada
 - Eliminar objetos en base de datos simulada

   *Para ejecutarlo de manera individual se ejecuta el siguiente comando:*
      ```
      pytest -s tests/test_unitary.py
      ```
![Imagen](/images/image-1.png)
   

2. En test_integration.py evaluamos los siguientes elementos:
 - Añadir objetos en base de datos real
 - Editar objetos en base de datos real
 - Eliminar objetos en base de datos real

    *Para ejecutarlo de manera individual se ejecuta el siguiente comando:*
      ```
      python -m unittest discover -s tests -p "test_integration.py"
      ```
![Imagen](/images/image-2.png)


3. En test_functionality.py evaluamos los siguientes elementos:
 - Añadir objetos con campos vacios
 - Editar objetos con campos vacios

   Necesitamos crear el archivo *init_db.py*, donde definimos una base de datos temporal local con la misma estructura para hacer las pruebas. Que tras ser usada se borra.

    *Para ejecutarlo de manera individual se ejecuta el siguiente comando:*
      ```
      python -m unittest tests.test_functionality
      ```
![Imagen](/images/image-3.png)


4. En test_performance.py evaluamos los siguientes elementos:
 - Ejecución de acceder, añadir y borrar un objeto por varios usuarios simultaneamente.

    *Antes de ser ejecutado, la pagina debe estar activa en otro sitio (terminal, consola, ...)*
      ```
      python app.py
      ```

    *Para ejecutarlo de manera individual se ejecuta el siguiente comando:*
      ```
      locust -f tests/test_performance.py --host=http://localhost:5000
      ```
![Imagen](/images/image-4.png)


5. En test_quality.py evaluamos la calidad de los tests recomendado mejoras y buenas prácticas.

   *Para ejecutarlo de manera individual se ejecuta el siguiente comando:*
      ```
      python tests/test_quality.py
      ```
![Imagen](/images/image-5.png)


6. En test_security.sh evaluamos los siguientes elementos:
 - Observar la imagen por seguridad

   Se tiene que descargar Trivy ejecutando el siguiente comando:
   ```
   sudo apt-get install -y wget && wget https://github.com/aquasecurity/trivy/releases/download/v0.46.0/trivy_0.46.0_Linux-64bit.deb && sudo dpkg -i trivy_0.46.0_Linux-64bit.deb
   ```
   *Para ejecutarlo de manera individual se ejecuta el siguiente comando:*
      ```
      ./tests/test_security.sh
      ```

![Imagen](/images/image-6.png)


Dentro del código en la parte de **test** de GithubActions vamos a realizar los siguientes acciones:

- Ejecutar el test unitario
- Ejecutar el test de integración
- Ejecutar el test de funcinalidad
- Ejecutar el test de rendimiento
- Ejecutar el test de calidad
- Ejecutar el test seguridad


## 5. Release

Definimos como se va a hacer el proceso de versionado del proyecto, en este caso creamos un tag para las versiones con la siguiente estructura:
 - Se añade la fecha en formato **año_mes_dia**
 - Se añade la fecha en formato **hora_minuto_segundo**


Dentro del código en la parte de **release** de GithubActions vamos a realizar los siguientes acciones:
- Versionado del contenido con fecha y hora

## 6. Deploy / Infraestructure



## 7. Operate


Dentro del código en la parte de **infraestructure** de GithubActions vamos a realizar los siguientes acciones:


## 8. Monitor

Dentro del código en la parte de **monitor** de GithubActions vamos a realizar los siguientes acciones:
