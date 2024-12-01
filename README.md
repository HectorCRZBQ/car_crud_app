# CAR_CRUD_APP

La idea del proyecto es implementar un ciclo CI/CD completo sobre una aplicación CRUD básica de gestión de inventario de vehículos.

Las fases a seguir van a ser:

1. Plan (Notion)
2. Code (Python)
3. Build (GithubActions)
4. Test (Pytest (Test generales) + Locust (Test de rendimiento) +  Trivy (Test de seguridad) )
5. Release (Jenkins / Git tagging)
6. Deploy (AWS / Google Cloud)
7. Operate (Terraform)
8. Monitor (Grafana o Prometheus (Back) y Google Analytics (Front))

## 1. Plan 

Planificación en Notion: https://www.notion.so/car_crud_app-14f7a0c76b9780d9af6ad93edb027a83?pvs=4

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


## 4. Test


## 5. Release


## 6. Deploy


## 7. Operate


## 8. Monitor