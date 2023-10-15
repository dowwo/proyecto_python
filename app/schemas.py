from typing import List, Union

from pydantic import BaseModel

class TareaBase(BaseModel):
    titulo: str
    descripcion: Union[str, None] = None

class TareaCreate(TareaBase):
    pass

class Tarea(TareaBase):
    id: int

    class Config:
        orm_mode = True

class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool
    # Usuario va abajo de Tarea ya que python no reconoce la clase por el orden de ejecución
    tareas: List[Tarea] = []

    class Config:
        orm_mode = True
    





