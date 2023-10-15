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

