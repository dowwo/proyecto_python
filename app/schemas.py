from typing import List, Union

from pydantic import BaseModel

from datetime import date

class TareaBase(BaseModel):
    titulo: str
    descripcion: Union[str, None] = None
    fecha_vencimiento: date
    activa: bool

class TareaCreate(TareaBase):
    pass

class TareaUpdateEstado(BaseModel):
    activa: bool

class TareaDelete(BaseModel):
    detail: str

class Tarea(TareaBase):
    id: int

    class ConfigDict:
        from_attributes = True

class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str

class UserUpdate(UserBase):
    hashed_password: str

# Para esta respuesta hay que usar BaseModel, ya que si usamos UserBase
# Ya devuelve un email en la respuesta, que no necesitamos al eliminar
# Al menos en la respuesta JSON
class UserDelete(BaseModel):
    detail: str

class User(UserBase):
    id: int
    is_active: bool
    # Usuario va abajo de Tarea ya que python no reconoce la clase por el orden de ejecución
    tareas: List[Tarea] = []

    class ConfigDict:
        
        from_attributes = True
    





