Softies Project
Softies es un asistente de voz inteligente que permite a los usuarios interactuar con sus proyectos mediante comandos de voz. Desarrollado como parte del proyecto de Ingeniería del Software, Softies integra reconocimiento de voz, procesamiento del lenguaje natural y una interfaz web intuitiva para facilitar la gestión de proyectos.

Características
🎙️ Reconocimiento de voz: Utiliza modelos de Vosk para transcribir comandos de voz en tiempo real.

🧠 Procesamiento del lenguaje natural: Interpreta y responde a comandos utilizando modelos de lenguaje avanzados.

🗂️ Gestión de proyectos: Crea, elimina y navega entre proyectos fácilmente.

🌐 Interfaz web interactiva: Diseñada con HTML, CSS y JavaScript para una experiencia de usuario fluida.

⚙️ Configuraciones personalizables: Ajusta preferencias y gestiona claves API desde la sección de configuración.

Requisitos
Python 3.8 o superior

pip (gestor de paquetes de Python)

Instalación
Clona el repositorio:

bash
Copiar
Editar
git clone https://github.com/Marlu0/softies_project.git
cd softies_project
Crea y activa un entorno virtual (opcional pero recomendado):

bash
Copiar
Editar
python -m venv env
source env/bin/activate  # En Windows: env\Scripts\activate
Instala las dependencias:

bash
Copiar
Editar
pip install -r requirements.txt
Ejecuta la aplicación:

bash
Copiar
Editar
python app.py
La aplicación estará disponible en http://localhost:5000.

Estructura del Proyecto
bash
Copiar
Editar
softies_project/
├── models/                 # Modelos de Vosk para reconocimiento de voz
├── src/                    # Código fuente principal
├── static/                 # Archivos estáticos (CSS, JS, imágenes)
├── templates/              # Plantillas HTML para la interfaz web
├── test/                   # Pruebas unitarias y de integración
├── app.py                  # Archivo principal para iniciar la aplicación
├── requirements.txt        # Lista de dependencias del proyecto
├── pipeline.drawio         # Diagrama del flujo de la aplicación
├── README.md               # Este archivo
└── HELP.md                 # Documentación adicional y preguntas frecuentes
Uso
Inicio: Al ejecutar la aplicación, accede a http://localhost:5000 en tu navegador.

Crear Proyecto: Haz clic en "Create new project" y selecciona la carpeta deseada.

Interacción por Voz: Utiliza el micrófono para dar comandos y gestionar tus proyectos.

Configuración: Accede a la sección de configuración para ajustar preferencias y gestionar claves API.

Contribuciones
¡Las contribuciones son bienvenidas! Si deseas mejorar Softies:

Haz un fork del repositorio.

Crea una nueva rama para tu funcionalidad (git checkout -b nueva-funcionalidad).

Realiza tus cambios y haz commits descriptivos.

Envía un pull request detallando tus modificaciones.

Equipo de Desarrollo
Marcel Manzano - u231726

Franco Olano - u233420

Nerea González - u199125

Adrià López - u233501

Berta Noguera - u199893

Adrià Porta - u215229

Francesc Baiget - u232665
