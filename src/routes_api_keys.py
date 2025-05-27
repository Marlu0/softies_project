# routes_api_keys.py  (o donde tengas tus rutas)

from flask import Blueprint, request, jsonify, abort
from database import get_api_keys, create_api_key, update_api_key, delete_api_key  # ya los tienes
from api_handler import is_valid_api_key                      # tu función de validación

bp_api_keys = Blueprint("api_keys", __name__, url_prefix="/api/api_keys")

@bp_api_keys.get("/")
def list_keys():
    """Devuelve todas las claves guardadas."""
    return jsonify(get_api_keys())           # → 200 OK  +  [{"name":"personal","key":"****"}, ...]

@bp_api_keys.post("/")
def add_key():
    data = request.get_json(force=True)
    key   = data.get("key", "").strip()
    name  = data.get("name", "default").strip() or "default"

    if not key:
        abort(400, description="API-Key vacía.")
    if not is_valid_api_key(key):
        abort(400, description="API-Key inválida.")

    create_api_key(name, key)
    return jsonify({"status": "ok"}), 201    # 201 Created

@bp_api_keys.put("/<string:name>")
def edit_key(name):
    data = request.get_json(force=True)
    new_key = data.get("key", "").strip()

    if not new_key:
        abort(400, description="API-Key vacía.")
    if not is_valid_api_key(new_key):
        abort(400, description="API-Key inválida.")

    update_api_key(name, new_key)
    return jsonify({"status": "updated"})    # 200 OK

@bp_api_keys.delete("/<string:name>")
def remove_key(name):
    delete_api_key(name)
    return "", 204                           # 204 No-Content
