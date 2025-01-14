# CAR_CRUD_APP

### La idea del proyecto es implementar un ciclo CI/CD completo sobre una aplicación CRUD básica de gestión de inventario de vehículos.

Las fases a seguir van a ser:

1. Plan (Notion)
2. Code (Python)
3. Build (GithubActions)
4. Test (Pytest (Test generales) + Locust (Test de rendimiento) +  Trivy (Test de seguridad) )
5. Operate (Terraform)
6. Deploy (AWS / Google Cloud) + KMS

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


## 5. Operate / Infraestructure

Se defiene la funcionalidad de Terraform para configurar y definir la estructura del AWS.

Añadimos a la estructura de proyecto los siguientes elementos:
 - Creamos el directorio **iac** donde guardamos los distintos códigos que Terraform va a hacer uso:
    - main.tf -> se define el bucket que se va a usar para almacenar el contenido y sus especificaciones.
    - variables.tf -> se declaran las variables reutilizables, en este caso la región
    - output.tf -> se define el contenido a mostrar tras que se realice el despliegue facilitando el acceso a los datos generados.
    - backend.tf -> backend de almacenamiento del tfstate en S3 y Dyanmo DB

La infraestructura que monta el archivo main.tf es:

- **VPC principal** (`aws_vpc.main`): Red privada en la que se encuentran los recursos.
- **Subred pública** (`aws_subnet.main`): Subred pública asociada a la VPC, permite el acceso desde Internet.
- **Puerta de enlace de Internet** (`aws_internet_gateway.main`): Habilita el acceso a Internet desde la VPC.
- **Tabla de rutas** (`aws_route_table.main`): Define las rutas dentro de la VPC.
- **Grupo de seguridad** (`aws_security_group.allow_http`): Configura reglas de firewall para permitir tráfico HTTP, SSH y en el puerto 5000.
- **Clave SSH** (`aws_key_pair.web_key`): Clave privada para acceder a la instancia EC2.
- **Instancia EC2** (`aws_instance.web`): Instancia en EC2 que ejecuta la aplicación web, accesible a través de SSH y HTTP.

La infraestructura que monta el archivo backend.tf es:

- **S3 Bucket** (`mi-bucket-terraform-state`): Crea un bucket de S3.
- **DynamoDB Table** (`tabla-de-lock-terraform`): Asegura que solo un proceso de Terraform realice cambios a la vez.
- **Backend de S3**: El archivo de estado de Terraform se almacena en un bucket de S3. La tabla de DynamoDB se utiliza para el bloqueo de estado.

Este formato en Markdown mostrará los nombres de las infraestructuras en **negrita**.


Todos estos pasos se ejecutan dentro de la carpeta de iac

   ```
   cd iac
   ```

Los pasos que se deben ejecutar con Terraform son los siguientes:

 - Infraestructura del backend de S3 y DynamoDB

   Creacion del bucket y de la tabla

   Para realizar este paso se ejcuta el siguiente comando:
   ```
   aws s3 mb s3://mi-bucket-terraform-state --region eu-west-1

   aws dynamodb create-table \
   --table-name tabla-de-lock-terraform \
   --attribute-definitions AttributeName=LockID,AttributeType=S \
   --key-schema AttributeName=LockID,KeyType=HASH \
   --provisioned-throughput ReadCapacityUnits=5,WriteCapacityUnits=5 \
   --region eu-west-1
   ```

   ![Imagen](/images/image-8.png)


 - Inicializacion de Terraform

   Descarga contenido necesario y se prepara el entorno.

   Para realizar este paso se ejcuta el siguiente comando:
   ```
   terraform init -backend=false
   ```

   ![Imagen](/images/image-9.png)


 - Actualización de los valores

   Para realizar este paso se ejcuta el siguiente comando:
   ```
   terraform init -reconfigure
   ```

   ![Imagen](/images/image-10.png)


 - Planificación de Terraform

   Define el pamn de ejecución con los cambios necesarios a realizar para satisfacer la estructura propuesta.

   Para realizar este paso se ejcuta el siguiente comando:
   ```
   terraform plan -out=tfplan
   ```

   ![Imagen](/images/image-11.png)
   ![Imagen](/images/image-12.png)


 - Aplicación de Terraform

   Se crean, actualizan o eliminan los recursos necesarios de la nube.

   Para realizar este paso se ejcuta el siguiente comando:
   ```
   terraform apply -auto-approve tfplan
   ```
   ![Imagen](/images/image-13.png)

 - Extraemos el valor de la IP publica de la instancia de EC2
   
   ```
   terraform output instance_public_ip
   ```

   ![Imagen](/images/image-14.png)

 - Copiamos el valor de la clave PEM generada por terraform y la alamcenamos dentro de ssh

   ```
   terraform output -raw private_key > ~/.ssh/web_key.pem
   ```

   ![Imagen](/images/image-15.png)
   ![Imagen](/images/image-16.png)

 - Verificamos los permisos necesarios de la clave privada

   ```
   chmod 400 ~/.ssh/web_key.pem

   ls -la # Lo revisamos en el directorio .ssh que contiene la clave web_key.pem
   ```
   
   ![Imagen](/images/image-17.png)

   ![Imagen](/images/image-18.png)

Dentro del código en la parte de **infraestructure** de GithubActions vamos a realizar los siguientes acciones:

 - Inicializacion
 - Planificación
 - Aplicacion
 - Obtencion de salidas

## 6. Deploy

Para el deploy vamos a usar Amazon Web Service.

El usuario va a tener qye tener las siguientes politicas:

 - **AmazonEC2FullAccess**
 - **AmazonS3FullAccess**
 - **AmazonVPCFullAccess**
 - **AWSKeyManagementServicePowerUser**
 - **GitHubActionsKMSDecryptPolicy**:

   ```
   {
      "Version": "2012-10-17",
      "Statement": [
         {
            "Effect": "Allow",
            "Action": "kms:Decrypt",
            "Resource": "arn:aws:kms:${Region}:${AccountId}:key/${KMSKeyId}"
         }
      ]
   }
   ```

 - **TerraformDynamoDBLockPolicy**: 

   ```
   {
      "Version": "2012-10-17",
      "Statement": [
         {
            "Effect": "Allow",
            "Action": [
               "dynamodb:CreateTable",
               "dynamodb:DeleteTable",
               "dynamodb:PutItem",
               "dynamodb:GetItem",
               "dynamodb:UpdateItem",
               "dynamodb:DeleteItem"
            ],
            "Resource": "arn:aws:dynamodb:${Region}:${AccountId}:table/${DynamoDBTableName}"
         }
      ]
   }
   ```

Los valores del usuario creados los incorporamos como Secretos dentro de Github para que los Gihub Actions:

 - AWS_ACCESS_KEY_ID: Tu Access Key del usuario IAM creado.
 - AWS_SECRET_ACCESS_KEY: Tu Secret Access Key del usuario IAM creado.
 - AWS_REGION: La región de AWS donde desplegarás los recursos (por ejemplo, eu-west-1).

Tambien tenemos que añadir el valor que tenemos en secrets.yaml como secreto para que siga estando funcional la conexión a la base de datos
  - MONGODB_URI: mongodb+srv://<db_user>:<db_password>@<db_name>.gtphu.mongodb.net/?retryWrites=true&w=majority&appName=<db_name>

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
   aws kms encrypt \
   --key-id <KMS_KEY_ID> \
   --plaintext fileb://secrets.yaml \
   --region <AWS_REGION> \
   --output text \
   --query CiphertextBlob | base64 > secrets.yaml.enc

   ```
Nos genera un archivo secrets.yaml.enc

El valor de KMS es un secreto del repositorio de Github, bajo el nombre KMS_KEY_ID.

Y para que se desencripte se hace uso del siguiente comando:
   ```
   aws kms decrypt \
   --ciphertext-blob fileb://secrets.yaml.enc \
   --output text \
   --query Plaintext \
   --region <AWS_REGION> | base64 --decode > secrets.yaml

   ```

Dentro del código en la parte de **deploy** de GithubActions vamos a realizar los siguientes acciones:

 - Definir y configurar los credenciales de AWS que vamos a usar
 - Descargar los artefactos construidos
 - Despliegue en el EC2
 - Copia de los archivos dentro de EC2


 Una vez que se haya creado todo la infraestructura necesaria, se puede realizar el despliegue:

Accedemos al directorio de .ssh:
   ```
   cd .ssh
   ```

  - Accedemos a la instancia EC2

   ```
   ssh -i ~/.ssh/web_key.pem ubuntu@<IP_PUBLICA>
   ```

   ![Imagen](/images/image-19.png)

   
  - Instalamos las dependencias necesarias
   ```
   sudo apt update
   sudo apt install -y python3-pip python3-venv
   ```

   ![Imagen](/images/image-20.png)
   ![Imagen](/images/image-21.png)


  - Creamos el entorno de la aplicacion
   ```
   mkdir ~/car_crud_app && cd ~/car_crud_app
   python3 -m venv venv
   source venv/bin/activate
   ```

   ![Imagen](/images/image-22.png)
   ![Imagen](/images/image-23.png)
   
Accedemos al directorio de iac:

   ```
   cd iac
   ```

  - Copiamos los archivos a dentro de la instancia de EC2

  Se copian los archivos necesarios al interior del EC2

   ```
   scp -i ~/.ssh/web_key.pem -r ~/Escritorio/car_crud_app/static ~/Escritorio/car_crud_app/templates ~/Escritorio/car_crud_app/app.py ~/Escritorio/car_crud_app/requirements2.txt ~/Escritorio/car_crud_app/secrets.yaml ubuntu@<IP_PUBLICA>:~/car_crud_app/
   ```

   ![Imagen](/images/image-24.png)
   ![Imagen](/images/image-25.png)

Accedemos al directorio de .ssh:

  - Instalar las dependencias de tu aplicación

   ```
   pip install -r requirements2.txt
   ```

   En este caso como usa la verision 3.8.10 se necesista el siguiente requirements2.txt:

   ```
   Flask==2.1.0
   Flask-Cors==3.0.10
   Flask-Login==0.5.0
   pymongo[srv]==3.12.1
   pyyaml==5.4.1
   Werkzeug==2.0.2
   ```

   ![Imagen](/images/image-26.png)


  - Dependencias necesaria para MongoDb Atlas

  sudo apt-get update
sudo apt-get install ca-certificates


  - Ejecuta la aplicación Flask

   ```
   flask run --host=0.0.0.0
   ```

   ![Imagen](/images/image-27.png)


Direcciones que acepta MongoDB Atlas:

![Imagen](/images/image-29.png)


Acceso desde el navegador a visualizar la página:

   ```
   http://<IP_PUBLICA>:5000
   ```

   ![Imagen](/images/image-28.png)


## Funcionamiento del pipeline:

### Video ejecucción pipeline

En este video, explico la ejecución del pipeline paso a paso y las tecnologías que uso.

[![Ejecución del Pipeline](https://img.youtube.com/vi/F-NrZsKntZ4/0.jpg)](https://youtu.be/F-NrZsKntZ4)

### Ejecución del Pipeline paso a paso

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
![Imagen](/images/image-39.png)

Tenemos desplegado la instancia EC2 en AWS:

![Imagen](/images/image-40.png)

Tenemos desplegado el bucket S3 en AWS:

![Imagen](/images/image-41.png)

Y se almacena dentro el terraform.tfstate

![Imagen](/images/image-42.png)

Tenemos la tabla de DynamoDB en AWS:

![Imagen](/images/image-43.png)

Tenemos el VPC en AWS:

![Imagen](/images/image-44.png)

Pares de claves en AWS:

![Imagen](/images/image-45.png)

Tenemos el KMS en AWS:

![Imagen](/images/image-46.png)


Una vez que se finelice de ejecutar el pipeline, dentro de la interfaz podemos realizar acciones como:

### Añadir vehiculos

[![Añadir Vehículos](https://img.youtube.com/vi/0nsQHS-mCyk/0.jpg)](https://youtu.be/0nsQHS-mCyk)


### Modificar vehiculos

 [![Editar Vehículos](https://img.youtube.com/vi/rDuOW0s1ZoM/0.jpg)](https://youtu.be/rDuOW0s1ZoM)


### Eliminar vehiculos

 [![Borrar Vehículos](https://img.youtube.com/vi/4E1obdL1wbw/0.jpg)](https://youtu.be/4E1obdL1wbw)

## Limpieza de la ejecucción

Para evitar costos no deseados es importante eliminar los recursos que no sean necesarios.

Para ello se ejecutan los siguientes comandos

   ```
   cd iac
   terraform destroy
   ```

![Imagen](/images/image-47.png)

![Imagen](/images/image-48.png)

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
   │   ├── backend.tf
   │   ├── .terraform
   │   ├── .terraform.lock.hcl
   │   └── variables.tf
   ├── images
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
   ├── requirements2.txt
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

--- 

### Hector de la Cruz Baquero - [Linkdedin](https://www.linkedin.com/in/h%C3%A9ctor-de-la-cruz-baquero-ba193429b/) - [Webpage](https://hectorcrzbq.github.io/)