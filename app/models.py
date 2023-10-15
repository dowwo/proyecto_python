from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Date
from sqlalchemy.orm import relationship

from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String) # Todavia no se si hacer el hash
    is_active = Column(Boolean, default=True)

    tareas = relationship("Tarea", back_populates="owner")

class Tarea(Base):
    __tablename__ = "tareas"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String, index=True)
    descripcion = Column(String, index=True)
    fecha_vencimiento = Column(Date, index=True)
    activa = Column(Boolean, default=True)

    owner = relationship("User", back_populates="tareas")



