# 🧠 Softies Project

**Softies** is an intelligent voice assistant that allows users to interact with their projects using voice commands. Developed as part of the Software Engineering project, Softies integrates speech recognition, natural language processing, and an intuitive web interface to simplify project management.

## ✨ Features

- 🎙️ **Speech Recognition**: Uses Vosk models to transcribe voice commands in real time.  
- 🧠 **Natural Language Processing**: Interprets and responds to commands using advanced language models.  
- 🗂️ **Project Management**: Easily create, delete, and navigate between projects.  
- 🌐 **Interactive Web Interface**: Built with HTML, CSS, and JavaScript for a smooth user experience.  
- ⚙️ **Customizable Settings**: Adjust preferences and manage API keys from the settings section.

## 🧰 Requirements

- Python 3.8 or higher  
- pip (Python package manager)

## 🚀 Installation

**1. Clone the repository:**

```bash
git clone https://github.com/Marlu0/softies_project.git
cd softies_project
2. (Optional but recommended) Create and activate a virtual environment:

bash
Copiar
Editar
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate
3. Install the dependencies:

bash
Copiar
Editar
pip install -r requirements.txt
4. Run the application:

bash
Copiar
Editar
python app.py
5. Open the app in your browser:
👉 http://localhost:5000

## 🗂️ Project Structure
bash
Copiar
Editar
softies_project/
├── models/                 # Vosk models for speech recognition
├── src/                    # Main source code
├── static/                 # Static files (CSS, JS, images)
├── templates/              # HTML templates for the web interface
├── test/                   # Unit and integration tests
├── app.py                  # Main file to start the app
├── requirements.txt        # Project dependencies
├── pipeline.drawio         # Application flow diagram
├── README.md               # This file
└── HELP.md                 # FAQ and additional documentation
🧑‍💻 Usage
Start: After running the app, go to http://localhost:5000

Create a project: Click "Create new project" and select a folder

Voice interaction: Use your microphone to manage projects with voice commands

Settings: Access "Settings" to configure options or manage your API keys

##⚠️ Important Note
This project is intended to run locally, so make sure to clone it and run it using Python to ensure everything works properly.


##👨‍🔧 Development Team
Marcel Manzano — u231726

Franco Olano — u233420

Nerea González — u199125

Adrià López — u233501

Berta Noguera — u199893

Adrià Porta — u215229

Francesc Baiget — u232665
