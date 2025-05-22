import os
import google.generativeai as genai

# Define the directory and full path for the API key file
API_KEY_DIR = "../data"
API_KEY_FILE = os.path.join(API_KEY_DIR, "api_key.txt")

def is_valid_api_key(api_key):
    """
    Verifica si la API key es válida intentando inicializar un modelo de Gemini.
    """
    try:
        genai.configure(api_key=api_key)
        list(genai.list_models())  # Verifica autenticación
        return True
    except Exception as e:
        print(f"Error al validar la API key: {e}")
        return False

def read_api_key_from_file():
    """Lee la API key desde el archivo."""
    try:
        with open(API_KEY_FILE, "r") as f:
            return f.readline().strip()
    except FileNotFoundError:
        return None

def save_api_key_to_file(api_key):
    """Guarda la API key en el archivo."""
    os.makedirs(API_KEY_DIR, exist_ok=True)
    with open(API_KEY_FILE, "w") as f:
        f.write(api_key + "\n")

def get_api_key():
    """
    Obtiene la API key. Primero intenta leerla desde un archivo.
    Si no existe o no es válida (comprobando con la API), se le pide al usuario y se guarda.
    """
    api_key = read_api_key_from_file()

    while not api_key or not is_valid_api_key(api_key):
        print("La API key no es válida o no se encontró.")
        api_key = input("Por favor, introduce tu API key de Google Gemini: ").strip()
        save_api_key_to_file(api_key)
        genai.configure(api_key=api_key)

    return api_key

# Test the API key validation
if __name__ == "__main__":
    api = get_api_key()
    print("API Key válida de Gemini obtenida y configurada.")

    try:
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content("¿Cuál es la capital de España?")
        print(f"Respuesta de prueba: {response.text}")
    except Exception as e:
        print(f"Error al usar la API después de la validación: {e}")
