from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError, ConnectionFailure
from bson.objectid import ObjectId
from datetime import datetime, timedelta
from typing import Optional, List, Dict
import os

class GestorTareas:
    def __init__(self, uri: str = 'mongodb://localhost:27017/'):
        """Inicializar conexión a MongoDB"""
        try:
            self.cliente = MongoClient(uri, serverSelectionTimeoutMS=5000)
            self.cliente.admin.command('ping')
            self.db = self.cliente['gestor_tareas']
            self.tareas = self.db['tareas']
            self.usuarios = self.db['usuarios']
            
            # Crear índices necesarios
            self._crear_indices()
            print("✅ Conectado a MongoDB")
        except ConnectionFailure:
            print("❌ Error: No se pudo conectar a MongoDB")
            raise
    
    def _crear_indices(self):
        """Crear índices para mejorar rendimiento"""
        self.usuarios.create_index("email", unique=True)
        self.tareas.create_index([("usuario_id", 1), ("fecha_creacion", -1)])
        self.tareas.create_index("estado")
    
    def crear_usuario(self, nombre: str, email: str) -> Optional[str]:
        """Crear un nuevo usuario"""
        try:
            resultado = self.usuarios.insert_one({
                "nombre": nombre,
                "email": email,
                "fecha_registro": datetime.now(),
                "activo": True
            })
            return str(resultado.inserted_id)
        except DuplicateKeyError:
            print(f"❌ Error: El email {email} ya está registrado")
            return None
    
    
    
     def obtener_usuario(self, correo_id: pass1:str) -> Optional[Dict]:
        """Obtener usuario por ID"""
        try:
              correo = self.usuarios.find_one({"email": ObjectId(email)})
            if correo:
                #verificar el password tecleado  por el usuario  con la base de datos 
                #Regresar datos del usuario
                #usuario['_id'] = str(usuario['_id'])
            return usuario
        except Exception as e:
            print(f"Error al obtener usuario: {e}")
            return None
    
    
    
    

       
            
    # Cerrar conexión
    gestor.cerrar_conexion()

if __name__ == "__main__":
    ejemplo_uso()