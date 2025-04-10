
# 🧾 Despliegue de Scraper en Google Cloud Run Jobs

Este proyecto automatiza el despliegue de un job de scraping usando Docker y Google Cloud Run Jobs. A continuación, se detallan los pasos para preparar el entorno, configurar los servicios en Google Cloud y desplegar correctamente el proyecto.

---

## 📌 1. Prerrequisitos del sistema

Antes de comenzar, asegurate de tener lo siguiente instalado y funcionando:

### 🛠️ Instalaciones necesarias

- [x] **Python 3.13** o compatible. Verificar con:
  ```bash
  python --version
  ```
- [x] **Docker**: https://www.docker.com/products/docker-desktop
- [x] **Google Cloud SDK (gcloud)**: https://cloud.google.com/sdk/docs/install

### 🧰 Configuración del entorno en Windows (opcional)

Si usás Git Bash o WSL en Windows, añadí lo siguiente a tu archivo `~/.bashrc` para evitar errores de entorno:

```bash
# Google Cloud SDK en Windows
if [ -f "/mnt/c/Users/<TU_USUARIO>/AppData/Local/Google/Cloud SDK/google-cloud-sdk/path.bash.inc" ]; then
    source "/mnt/c/Users/<TU_USUARIO>/AppData/Local/Google/Cloud SDK/google-cloud-sdk/path.bash.inc"
fi
if [ -f "/mnt/c/Users/<TU_USUARIO>/AppData/Local/Google/Cloud SDK/google-cloud-sdk/completion.bash.inc" ]; then
    source "/mnt/c/Users/<TU_USUARIO>/AppData/Local/Google/Cloud SDK/google-cloud-sdk/completion.bash.inc"
fi
```

Luego ejecutá:

```bash
source ~/.bashrc
```

---

## ☁️ 2. Configuración de Google Cloud

### 🔐 Autenticación y configuración del proyecto

```bash
gcloud auth login
gcloud config set project <ID_DEL_PROYECTO>
gcloud config set compute/region southamerica-east1
```

### 👤 Crear una cuenta de servicio

1. Ir a: [IAM - Service Accounts](https://console.cloud.google.com/iam-admin/serviceaccounts)
2. Crear una nueva cuenta con los siguientes permisos:
   - Cloud Run Admin
   - Artifact Registry Writer
   - BigQuery Data Editor (según lo que use tu app)
3. Descargar la clave en formato JSON.
4. Guardar el archivo como `service_account.json` en la raíz del proyecto.


### 🔧 Habilitar APIs necesarias

```bash
gcloud services enable artifactregistry.googleapis.com run.googleapis.com
```


### 📦 Crear el repositorio en Artifact Registry

```bash
gcloud artifacts repositories create news-images   --repository-format=docker   --location=southamerica-east1   --description="Repositorio para imágenes Docker"
```

---

## 🚀 3. Despliegue del job

### 🧪 a) Crear el archivo `.env`

Ubicado en la raíz del proyecto, con el siguiente contenido:

```env
PROJECT_ID=ID_DEL_PROYECTO
REGION=TU_REGION
ARTIFACT_REPO=NOMBRE_ARTIFACT
IMAGE_NAME=NOMBRE_IMAGEN
SERVICE_NAME=NOMBRE_CUENTA_SERVICIO
```

### 🔐 b) Verificar `service_account.json`

Debe estar en la raíz del proyecto con las credenciales de la cuenta de servicio.

### 🧨 c) Ejecutar el script de despliegue

```bash
bash run.sh
```

Este script hace:

1. Carga las variables de entorno desde `.env`
2. Construye la imagen Docker
3. Sube la imagen al repositorio de Artifact Registry
4. Crea (o actualiza) un job en Cloud Run
5. Ejecuta el job automáticamente

### ▶️ d) Ejecución manual del job (opcional)

Si querés ejecutar el job manualmente luego del despliegue:

```bash
gcloud run jobs execute scraper-job --region=southamerica-east1
```

---

## 📂 Estructura del proyecto

```bash
.
├── app/                  # Módulos de procesamiento y scraping de datos
│   ├── bq_loader.py      # Script encargado de cargar los datos procesados a BigQuery         
│   ├── function.py       # Funciones auxiliares y utilitarias compartidas por otros módulos
│   ├── processor.py      # Lógica de transformación y limpieza de datos
│   └── scraper.py        # Módulo principal para realizar scraping web
├── scripts/              # Scripts relacionados al despliegue y automatización
│   └── deploy.sh         # Script que construye la imagen Docker y crea el job en Cloud Run
├── requirements.txt      # Archivo con las dependencias de Python necesarias para el proyecto
├── Dockerfile            # Configuración de la imagen Docker utilizada para el despliegue
├── .env                  # Variables de entorno sensibles (no debe subirse al repositorio)
├── service_account.json  # Credenciales de la cuenta de servicio de GCP (no debe subirse al repositorio)
├── main.py               # Punto de entrada principal del proyecto; orquesta los distintos módulos
├── run.sh                # Script general para ejecutar el flujo de despliegue o ejecución
└── README.md             # Documentación del proyecto

```

---

## 🧠 Notas adicionales

- Podés usar [Secret Manager](https://cloud.google.com/secret-manager) para manejar credenciales sensibles.
- Para ver logs del job:
  ```bash
  gcloud logging read "resource.type=cloud_run_job AND resource.labels.job_name=scraper-job" --limit 50
  ```

## 💬 Uso de ChatGPT

Se utilizó la herramienta para consultas sobre la estructuración del proyecto como tal para agilizar el proceso. Se adjunta el link del chat a continuación:

https://chatgpt.com/share/67f76040-3a98-800e-884c-3f755b62f571