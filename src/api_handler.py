import google.generativeai as genai
from typing import Optional, List, Dict
from database import get_api_keys, create_api_key

# ------------------------------------------------------------------
# Funciones auxiliares que YA existen en tu proyecto
# ------------------------------------------------------------------
# from tu_módulo_bd import get_db_connection       # ← ya lo tienes
# def create_api_key(name: str, key: str) -> None: ...
# def get_api_keys() -> List[Dict[str, str]]: ...
# ------------------------------------------------------------------


# ---------- Validación -------------------------------------------------
def is_valid_api_key(api_key: str) -> bool:
    """
    Comprueba si una API-Key de Gemini funciona inicializando la SDK.
    """
    try:
        genai.configure(api_key=api_key)
        # La llamada a list_models() fuerza la autenticación.
        _ = list(genai.list_models())
        return True
    except Exception as exc:
        print(f"❌  Error al validar la API-Key: {exc}")
        return False


# ---------- Almacenamiento / obtención ---------------------------------
def _get_first_valid_db_key() -> Optional[str]:
    """
    Devuelve la primera API-Key válida encontrada en la BD
    (o None si ninguna es válida).
    """
    for row in get_api_keys():                       # [{'id':1,'name':'…','key':'…'}, …]
        api_key = row["key"]
        if is_valid_api_key(api_key):
            print(f"✅  Usando API-Key '{row['name']}' almacenada en BD.")
            return api_key
    return None


def _store_api_key(name: str, api_key: str) -> None:
    """
    Guarda (o sobreescribe) una API-Key en la base de datos.
    Si ya existe una fila con el mismo name puedes decidir actualizarla;
    aquí simplemente insertamos una nueva fila.
    """
    create_api_key(name, api_key)
    print(f"💾  API-Key guardada en BD con el nombre '{name}'.")


# ---------- Orquestador principal -------------------------------------
def get_api_key() -> str:
    """
    Obtiene una API-Key válida:
    1. Busca en la BD y usa la primera que pase la validación.
    2. Si no hay ninguna válida, la pide al usuario, la valida y la guarda.
    """
    api_key = _get_first_valid_db_key()

    while not api_key:
        print("No se encontró ninguna API-Key válida en la base de datos.")
        api_key = input("Introduce tu API-Key de Google Gemini: ").strip()

        if not is_valid_api_key(api_key):
            print("La API-Key no es válida. Inténtalo de nuevo.\n")
            api_key = None
            continue

        alias = input("Asigna un nombre/alias para esta clave (p. ej. 'personal'): ").strip() or "default"
        _store_api_key(alias, api_key)

    # Configuramos la SDK con la clave que finalmente tengamos
    genai.configure(api_key=api_key)
    return api_key


# ---------- Ejemplo de uso --------------------------------------------
if __name__ == "__main__":
    api_key = get_api_key()
    print("\n🎉  API-Key válida configurada. Probando…\n")

    try:
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content("¿Cuál es la capital de España?")
        print("Respuesta de prueba:", response.text)
    except Exception as exc:
        print(f"⚠️  Error al consumir la API tras configurar la clave: {exc}")
