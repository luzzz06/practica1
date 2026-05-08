from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError, ConnectionFailure
from bson.objectid import ObjectId
from datetime import datetime, timedelta
from typing import Optional, List, Dict

class Gestortareas:
    def __init__(self, uri: str = 'mongodb://localhost:27017/'):
        try:
            self.cliente = MongoClient(uri, serverSelectionTimeoutMS=5000)
            self.cliente.admin.command('ping')
            self.db = self.cliente['Mis_Tareas']
            self.tareas = self.db['tareas']
            self.usuarios = self.db['usuarios']
            self._crear_indices()
            print("✅ Conexión exitosa a MongoDB")
        except ConnectionFailure:
            print("❌ Error: No se pudo conectar a MongoDB")
            raise

    def _crear_indices(self):
        try:
            self.usuarios.create_index("email", unique=True)
            self.tareas.create_index([("usuario_id", 1), ("fecha_creacion", -1)])
            self.tareas.create_index("estado")
            self.tareas.create_index([("titulo", "text"), ("descripcion", "text")], 
                                    name="titulo_text_descripcion_text")
        except Exception as e:
            if "IndexOptionsConflict" not in str(e):
                print(f"⚠️ Aviso en índices: {e}")

    def crear_usuario(self, user: str, email: str, secreto: str) -> bool:
        try:
            self.usuarios.insert_one({
                "user": user, "email": email, "secreto": secreto,
                "fecha_registro": datetime.now(), "activo": True
            })
            return True
        except DuplicateKeyError:
            return False

    def obtener_usuario_por_email(self, email: str) -> Optional[Dict]:
        return self.usuarios.find_one({"email": email})

    def obtener_usuario(self, usuario_id: str) -> Optional[Dict]:
        try:
            return self.usuarios.find_one({"_id": ObjectId(usuario_id)})
        except:
            return None

    def crear_tarea(self, usuario_id: str, titulo: str, estado: str = "pendiente") -> Optional[str]:
        if not self.obtener_usuario(usuario_id):
            return None
        tarea = {
            "usuario_id": ObjectId(usuario_id),
            "titulo": titulo,
            "estado": estado,
            "fecha_creacion": datetime.now(),
            "fecha_limite": datetime.now() + timedelta(days=7),
            "completada": estado == "completada"
        }
        resultado = self.tareas.insert_one(tarea)
        return str(resultado.inserted_id)

    def obtener_tareas_usuario(self, usuario_id: str) -> List[Dict]:
        cursor = self.tareas.find({"usuario_id": ObjectId(usuario_id)}).sort("fecha_creacion", -1)
        resultado = []
        for t in cursor:
            t['_id'] = str(t['_id'])
            t['usuario_id'] = str(t['usuario_id'])
            resultado.append(t)
        return resultado

    def actualizar_estado_tarea(self, tarea_id: str, nuevo_estado: str) -> bool:
        try:
            resultado = self.tareas.update_one(
                {"_id": ObjectId(tarea_id)},
                {
                    "$set": {
                        "estado": nuevo_estado,
                        "completada": nuevo_estado == "completada",
                        "fecha_modificacion": datetime.now()
                    }
                }
            )
            return resultado.modified_count > 0
        except:
            return False

    def eliminar_tarea(self, tarea_id: str) -> bool:
        try:
            resultado = self.tareas.delete_one({"_id": ObjectId(tarea_id)})
            return resultado.deleted_count > 0
        except:
            return False
    