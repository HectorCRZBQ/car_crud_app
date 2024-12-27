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
 - Añadir objetos en base de datos local de Mongo
 - Editar objetos en base de datos local de Mongo
 - Eliminar objetos en base de datos local de Mongo
 - Editar un objeto inexistente en la base de datos local de Mongo
 - Eliminar un objeto inexistente en la base de datos local de Mongo

    *Para ejecutarlo de manera individual se ejecuta el siguiente comando:*
      ```
      pytest -v tests/test_integration.py"
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

## 6. Deploy

Para el deploy vamos a usar Amazon Web Service, y para almacenar el contenido generado en este código vamos a usar un bucket S3.

El usuario que vamos a utilizar se uso para una práctica similar de despliegue en AWS. Como elemento destacable tiene asignada una politica personaliza :

   ```
   {
      "Version": "2012-10-17",
      "Statement": [
         {
            "Effect": "Allow",
            "Action": [
               "s3:CreateBucket",
               "s3:DeleteBucket",
               "s3:ListBucket",
               "s3:Get*",
               "s3:*Object",
               "s3:PutBucketPolicy",
               "s3:PutBucketPublicAccessBlock",
               "s3:PutBucketVersioning",
               "s3:PutBucketWebsite",
               "s3:GetBucketCORS",
               "s3:PutBucketCORS"
            ],
            "Resource": [
               "arn:aws:s3:::github-actions-pipeline-web-*",
               "arn:aws:s3:::github-actions-pipeline-web-*/*",
               "arn:aws:s3:::github-actions-pipeline-artifacts-*",
               "arn:aws:s3:::github-actions-pipeline-artifacts-*/*",
               "arn:aws:s3:::terraform-state-*",
               "arn:aws:s3:::terraform-state-*/*"
            ]
         },
         {
            "Effect": "Allow",
            "Action": [
               "dynamodb:CreateTable",
               "dynamodb:DeleteTable",
               "dynamodb:PutItem",
               "dynamodb:GetItem",
               "dynamodb:DeleteItem",
               "dynamodb:UpdateItem"
            ],
            "Resource": "arn:aws:dynamodb:*:*:table/terraform-lock"
         }
      ]
   }
   ```


Se va a hacer uso de la AWS CLI para definir los credenciales del usuario que hemos creado, y se usa el siguiente comando:

   ```
   aws configure
   ```

*Ejemplo de la interfaz de aws configure*

   ```
   AWS Access Key ID [*******************: ID del usuario (dentro del .csv)
   AWS Secret Access Key [******************]: Access Key del usuario (dentro del .csv)
   Default region name [eu-west-1]: 
   Default output format [None]:
   ```

Para encriptar el valor de secrets.yaml hacemos uso de KMS

Se encripta el valor de secrets.yaml en terminal con el siguiente comando:
   ```
   aws kms decrypt \
   --ciphertext-blob fileb://secrets.yaml.enc \
   --output text \
   --query Plaintext \
   --key-id <KMS_KEY_ID>\
   | base64 --decode > secrets.yaml

   ```
Nos genera un archivo secrets.yaml.enc

El valor de KMS es un secreto del repositorio de Github, bajo el nombre KMS_KEY_ID.

Necesitamos tener una clave SSH para que se puedan copiar los archivos dentro del EC2, para crearla se ejecuta:

   ```
   ssh-keygen -t rsa -b 2048 -f ~/.ssh/id_rsa -N ""

   cat ~/.ssh/id_rsa # Se copia el contenido dentro del secreto SSH_PRIVATE_KEY
   ```

El contenido que se obtiene se integra como un secreto con el nombre SSH_PRIVATE_KEY

Dentro del código en la parte de **deploy** de GithubActions vamos a realizar los siguientes acciones:

 - Definir y configurar los credenciales de AWS que vamos a usar
 - Descargar los artefactos construidos
 - Despliegue en bucket S3
 - Copia de los artefactos dentro del Bucket S3


## 7. Operate / Infraestructure

Se defiene la funcionalidad de Terraform para configurar y definir la estructura del AWS.

Añadimos a la estructura de proyecto los siguientes elementos:
 - Creamos el directorio **iac** donde guardamos los distintos códigos que Terraform va a hacer uso:
    - main.tf -> se define el bucket que se va a usar para almacenar el contenido y sus especificaciones.
    - variables.tf -> se declaran las variables reutilizables, en este caso la región
    - output.tf -> se define el contenido a mostrar tras que se realice el despliegue facilitando el acceso a los datos generados.

Todos estos pasos se ejecutan dentro de la carpeta de iac

   ```
   cd iac
   ```

Los pasos que se deben ejecutar con Terraform son los siguientes:
 - Inicializacion de Terraform

   Descarga contenido necesario y se prepara el entorno.

   Para realizar este paso se ejcuta el siguiente comando:
   ```
   terraform init
   ```

   ![Imagen](/images/image-8.png)


 - Planificación de Terraform

   Define el pamn de ejecución con los cambios necesarios a realizar para satisfacer la estructura propuesta.

   Para realizar este paso se ejcuta el siguiente comando:
   ```
   terraform plan
   ```

   ![Imagen](/images/image-9.png)
   ![Imagen](/images/image-10.png)


 - Aplicación de Terraform

   Se crean, actualizan o eliminan los recursos necesarios de la nube.

   Para realizar este paso se ejcuta el siguiente comando:
   ```
   terraform apply
   ```
   ![Imagen](/images/image-11.png)
   ![Imagen](/images/image-12.png)
   ![Imagen](/images/image-13.png)


Dentro de AWS podemos observar como tras todos los pasos se han creado los 

Los valores del usuario creados los incorporamos como Secretos:

 - AWS_ACCESS_KEY_ID: Tu Access Key del usuario IAM creado.
 - AWS_SECRET_ACCESS_KEY: Tu Secret Access Key del usuario IAM creado.
 - AWS_REGION: La región de AWS donde desplegarás los recursos (por ejemplo, eu-west-1).

Tambien tenemos que añadir el valor que tenemos en secrets.yaml como secreto para que siga estando funcional la conexión a la base de datos
  - MONGODB_URI: mongodb+srv://<db_user>:<db_password>@<db_name>.gtphu.mongodb.net/?retryWrites=true&w=majority&appName=<db_name>

   ![Imagen](/images/image-14.png)


Dentro del código en la parte de **infraestructure** de GithubActions vamos a realizar los siguientes acciones:

 - Inicializacion
 - Planificación
 - Aplicacion
 - Obtencion de salidas


## 8. Monitor

Dentro del código en la parte de **monitor** de GithubActions vamos a realizar los siguientes acciones:


## Funcionamiento del pipeline:

El pipeline se activará automáticamente con cada push a la rama main.

Ejecutamos el siguiente comando para añadir todas la modificaciones realizadas al commit:

```
   git add .
```
Redactamos un commit de que se han realizado cambios en el contenido del proyecto

```
   git commit -m "Update website content"
```
Y por ultimo lo pusheamos a la rama *main*

```
   git push origin main
```
![Imagen](/images/image-15.png)

Tenemos desplegado el Bucket S3 en AWS:

![Imagen](/images/image-16.png)

Tenemos la tabla de DynamoDB en AWS:

![Imagen](/images/image-17.png)


## Limpieza de la ejecucción

Para evitar costos no deseados es importante eliminar los recursos que no sean necesarios.

Para ello se ejecutan los siguientes comandos

   ```
   cd iac
   terraform destroy
   ```

Y sería necesario eliminar de manera manual los siguientes elementos:
 - El bucket de estado de Terraform
 - La tabla DynamoDB de bloqueo

## Estructura final del Proyecto

   ```
   ├── app.py
   ├── .git
   │   ├── branches
   │   ├── COMMIT_EDITMSG
   │   ├── config
   │   ├── description
   │   ├── HEAD
   │   ├── hooks
   │   ├── index
   │   ├── info
   │   ├── logs
   │   ├── objects
   │   ├── packed-refs
   │   └── refs
   ├── .github
   │   └── worflows
   ├── .gitignore
   ├── iac
   │   ├── main.tf
   │   ├── outputs.tf
   │   ├── .terraform
   │   ├── .terraform.lock.hcl
   │   └── variables.tf
   ├── images
   │   ├── image-10.png
   │   ├── image-11.png
   │   ├── image-12.png
   │   ├── image-13.png
   │   ├── image-14.png
   │   ├── image-1.png
   │   ├── image-2.png
   │   ├── image-3.png
   │   ├── image-4.png
   │   ├── image-5.png
   │   ├── image-6.png
   │   ├── image-7.png
   │   ├── image-8.png
   │   └── image-9.png
   ├── init_db.py
   ├── prompts.md
   ├── __pycache__
   │   ├── app.cpython-312.pyc
   │   └── init_db.cpython-312.pyc
   ├── .pytest_cache
   │   ├── CACHEDIR.TAG
   │   ├── .gitignore
   │   ├── README.md
   │   └── v
   ├── README.md
   ├── requirements.txt
   ├── scripts
   │   └── setup.sh
   ├── secrets.yaml
   ├── static
   │   └── styles.css
   ├── templates
   │   ├── add_car.html
   │   ├── base.html
   │   ├── edit_car.html
   │   └── index.html
   ├── tests
   │   ├── __init__.py
   │   ├── __pycache__
   │   ├── test_functionality.py
   │   ├── test_integration.py
   │   ├── test_performance.py
   │   ├── test_quality.py
   │   ├── test_security.sh
   │   └── test_unitary.py
   ├── .tool-versions
   └── venv
      ├── bin
      ├── include
      ├── lib
      ├── lib64 -> lib
      └── pyvenv.cfg
   ```