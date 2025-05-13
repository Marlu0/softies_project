import os
import google.generativeai as genai

def is_valid_api_key(api_key):
    """
    Verifica si la API key es válida intentando inicializar un modelo de Gemini.
    """
    try:
        genai.configure(api_key=api_key)
        # Intentamos listar los modelos para verificar la autenticación.
        # Si la clave no es válida, esto debería lanzar una excepción.
        list(genai.list_models())
        return True
    except Exception as e:
        print(f"Error al validar la API key: {e}")
        return False

def read_api_key_from_file(filename="api_key.txt"):
    """Lee la API key desde el archivo."""
    try:
        with open(filename, "r") as f:
            api_key = f.readline().strip()
        return api_key
    except FileNotFoundError:
        return None

def save_api_key_to_file(api_key, filename="api_key.txt"):
    """Guarda la API key en el archivo."""
    with open(filename, "w") as f:
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
        # Es importante configurar la API key globalmente después de obtenerla
        genai.configure(api_key=api_key)

    # Si llegamos aquí, la API key es válida y ya está configurada.
    return api_key

if __name__ == "__main__":
    api = get_api_key()
    print(f"API Key válida de Gemini obtenida y configurada.")

    # Puedes realizar una prueba simple para verificar que la API funciona
    try:
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content("¿Cuál es la capital de España?")
        print(f"Respuesta de prueba: {response.text}")
    except Exception as e:
        print(f"Error al usar la API después de la validación: {e}")