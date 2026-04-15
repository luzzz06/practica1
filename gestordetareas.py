 def obtener_usuario(self, correo_id: pass:str) -> Optional[Dict]:
        """Obtener usuario por ID"""
        try:
              correo = self.usuarios.find_one({"email": ObjectId(email)})
            if usuario:
                usuario['_id'] = str(usuario['_id'])
            return usuario
        except Exception as e:
            print(f"Error al obtener usuario: {e}")
            return None
    
    
    
    
    
    
    
    def crear_tarea(self, email_id: str, titulo: str, descripcion: str = "", 
                fecha_limite: Optional[datetime] = None) -> Optional[str]:
        """Crear una nueva tarea para un usuario"""
        # Verificar que el usuario existe
        if not self.obtener_usuario(usuario_id):
            print(f"❌ Error: Usuario {usuario_id} no existe")
            return None
 
 