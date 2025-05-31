
# 🧠 Softies Project

Softies es un asistente de voz inteligente que permite a los usuarios interactuar con sus proyectos mediante comandos de voz. Desarrollado como parte del proyecto de Ingeniería de Software, Softies integra reconocimiento de voz, procesamiento de lenguaje natural y una interfaz web intuitiva para simplificar la gestión de proyectos.

## ✨ Features
- 🎙️ **Reconocimiento de voz:** Utiliza modelos Vosk para transcribir comandos de voz en tiempo real.
- 🧠 **Procesamiento de lenguaje natural:** Interpreta y responde a comandos usando modelos avanzados.
- 🗂️ **Gestión de proyectos:** Crea, elimina y navega fácilmente entre proyectos.
- 🌐 **Interfaz web interactiva:** Construida con HTML, CSS y JavaScript para una experiencia fluida.
- ⚙️ **Configuración personalizable:** Ajusta preferencias y gestiona claves de API desde la sección de configuración.

## 🧰 Requisitos
- Python 3.8 o superior
- pip (administrador de paquetes de Python)

## 🚀 Instalación

Clona el repositorio:

```bash
git clone https://github.com/Marlu0/softies_project.git
cd softies_project
```

Crea y activa un entorno virtual (opcional pero recomendado):

```bash
python -m venv env
source env/bin/activate  # En Windows: env\Scripts\activate
```

Instala las dependencias:

```bash
pip install -r requirements.txt
```

Ejecuta la aplicación:

```bash
python app.py
```

Accede a la app en tu navegador:
👉 [http://localhost:5000](http://localhost:5000)

## 🗂️ Estructura del proyecto

```bash
softies_project/
├── models/                 # Modelos Vosk para reconocimiento de voz
├── src/                    # Código fuente principal
├── static/                 # Archivos estáticos (CSS, JS, imágenes)
├── templates/              # Plantillas HTML para la interfaz web
├── test/                   # Pruebas unitarias e integración
├── app.py                  # Archivo principal para iniciar la app
├── requirements.txt        # Dependencias del proyecto
├── pipeline.drawio         # Diagrama de flujo de la aplicación
├── README.md               # Este archivo
└── HELP.md                 # FAQ y documentación adicional
```

## 🧑‍💻 Uso
- **Inicio:** Una vez que la app esté en ejecución, abre [http://localhost:5000](http://localhost:5000) en tu navegador.
- **Crear proyecto:** Haz clic en "Crear nuevo proyecto" y selecciona una carpeta.
- **Interacción por voz:** Usa tu micrófono para gestionar proyectos mediante comandos de voz.
- **Configuraciones:** Dirígete a "Configuración" para ajustar opciones o gestionar claves de API.

## ⚠️ Nota importante
Este proyecto está diseñado para ejecutarse localmente, por lo que debe ser clonado y ejecutado con Python para garantizar su correcto funcionamiento.

## 🤝 Contribuciones
¡Las contribuciones son bienvenidas! Para colaborar:

1. Haz un fork del repositorio.
2. Crea una rama para la nueva funcionalidad:
    ```bash
    git checkout -b new-feature
    ```
3. Realiza cambios y confirma con descripciones claras.
4. Abre un pull request explicando tus modificaciones.

## 👨‍🔧 Equipo de desarrollo
- **Marcel Manzano** — u231726
- **Franco Olano** — u233420
- **Nerea González** — u199125
- **Adrià López** — u233501
- **Berta Noguera** — u199893
- **Adrià Porta** — u215229
- **Francesc Baiget** — u232665
```

Este formato mejora la legibilidad con una estructura clara, resaltando las secciones clave con negritas y enlaces bien formateados. ¡Espero que te sirva! 🚀
