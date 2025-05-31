# 🧠 Softies Project

**Softies** és un assistent de veu intel·ligent que permet als usuaris interactuar amb els seus projectes mitjançant comandes de veu. Desenvolupat com a part del projecte d'Enginyeria del Software, Softies integra reconeixement de veu, processament del llenguatge natural i una interfície web intuïtiva per facilitar la gestió de projectes.

---

## ✨ Característiques

- 🎙️ **Reconeixement de veu**: Utilitza models de **Vosk** per transcriure comandes de veu en temps real.  
- 🧠 **Processament del llenguatge natural**: Interpreta i respon comandes mitjançant models avançats de llenguatge.  
- 🗂️ **Gestió de projectes**: Crea, elimina i navega entre projectes fàcilment.  
- 🌐 **Interfície web interactiva**: Desenvolupada amb HTML, CSS i JavaScript per a una experiència fluïda.  
- ⚙️ **Configuracions personalitzables**: Ajusta preferències i gestiona claus API des de la secció de configuració.

---

## 🧰 Requisits

- Python **3.8** o superior  
- `pip` (gestor de paquets de Python)  

---

## 🚀 Instal·lació

### 1. Clona el repositori

```bash
git clone https://github.com/Marlu0/softies_project.git
cd softies_project
2. Crea i activa un entorn virtual (opcional però recomanat)
Linux/macOS:

bash
Copiar
Editar
python -m venv env
source env/bin/activate
Windows:

bash
Copiar
Editar
python -m venv env
env\Scripts\activate
3. Instal·la les dependències
bash
Copiar
Editar
pip install -r requirements.txt
4. Executa l'aplicació
bash
Copiar
Editar
python app.py
L'aplicació estarà disponible a:
👉 http://localhost:5000

🗂️ Estructura del Projecte
plaintext
Copiar
Editar
softies_project/
├── models/                 # Models Vosk per al reconeixement de veu
├── src/                    # Codi font principal
├── static/                 # Fitxers estàtics (CSS, JS, imatges)
├── templates/              # Plantilles HTML per la interfície web
├── test/                   # Tests unitaris i d'integració
├── app.py                  # Arxiu principal per iniciar l'app
├── requirements.txt        # Dependències del projecte
├── pipeline.drawio         # Diagrama de flux de l'aplicació
├── README.md               # Aquest arxiu
└── HELP.md                 # FAQ i documentació addicional
🧑‍💻 Ús
Inici: Un cop executada l'app, obre http://localhost:5000 al navegador.

Crear projecte: Fes clic a "Create new project" i selecciona la carpeta desitjada.

Interacció per veu: Usa el micròfon per gestionar projectes mitjançant comandes.

Configuració: Accedeix a la secció de configuració per ajustar opcions o gestionar les teves API Keys.

⚠️ Nota important:
Aquest projecte està pensat per funcionar localment, així que cal clonar-lo i executar-lo amb Python per garantir el funcionament correcte.

🤝 Contribucions
Les contribucions són benvingudes!
Per col·laborar:

bash
Copiar
Editar
# Fes un fork del repositori
# Crea una nova branca
git checkout -b nova-funcionalitat

# Realitza els canvis i fes commits clars
git add .
git commit -m "Nova funcionalitat afegida"

# Puja la branca i envia un pull request
git push origin nova-funcionalitat
👨‍🔧 Equip de Desenvolupament
Marcel Manzano — u231726

Franco Olano — u233420

Nerea González — u199125

Adrià López — u233501

Berta Noguera — u199893

Adrià Porta — u215229

Francesc Baiget — u232665
