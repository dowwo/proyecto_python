from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
# Respuesta a una solicitud POST para crear un usuario
@app.post("/users/", response_model=schemas.User)
# Recibe un email
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    # Si ya existe el email
    if db_user:
        # Arroja una HTTPException con código 400 y el detalle, emial ya registrado
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)

# Respuesta a una solicitud GET que devuelve los usuarios registrados
@app.get("/users/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

# Respuesta que devuelve una consulta de usuario por su id de usuario
@app.get("/users/{user_id}", response_model=schemas.User)
# Esta función recibe un id de usuario en la URL
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    # Si no existe
    if db_user is None:
        # Arroja una HTTPException con código 404
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return db_user

# Respuesta a la petición para modificar un usuario

# Respuesta a la solicitud DELETE para eliminar un usuario pasando su id en la URL
@app.delete("/users/{user_id}", response_model=schemas.UserDelete)
# Se pasa el id del usuario en la URL
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    # Si el usuario no existe
    if db_user is None:
        # Arroja una HTTPException con código 404
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    crud.delete_user_by_id(db=db, user_id=user_id)
    return {"detail": "Usuario eliminado correctamente"}

# endpoint POST para crear tarea
@app.post("/tareas/", response_model=schemas.Tarea)
def create_tarea(tarea: schemas.TareaCreate, user_id: int, db: Session = Depends(get_db)):
    db_tarea = models.Tarea(**tarea.dict(), owner_id=user_id)
    db.add(db_tarea)
    db.commit()
    db.refresh(db_tarea)
    return db_tarea
    
# Respuesta a la solicitud GET para listar todas las tareas
@app.get("/tareas/", response_model=List[schemas.Tarea])
def read_tareas(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    tareas = crud.get_tareas(db, skip=skip, limit=limit)
    return tareas

# Este bloque de código NO funciona
# @app.get("/tareas/{user_id}", response_model=schemas.Tarea)
# def read_tareas_by_user(user_id: int, skip: int = 0, limit: int = 100, activa: bool = None, db: Session = Depends(get_db)):
#     if activa is False: # False
#         tareas = crud.get_tarea(db, user_id=user_id, activa=False, skip=skip, limit=limit)
#     else: # True
#         tareas = crud.get_tarea(db, user_id=user_id, activa=True, skip=skip, limit=limit)  
#     if not tareas:
#         raise HTTPException(status_code=404, detail="No existen tareas para este usuario")
       
#     return tareas

@app.get("/tareas/{user_id}", response_model=schemas.Tarea)
def read_tareas_by_user(user_id: int, skip: int = 0, limit: int = 100, activa: bool = None, db: Session = Depends(get_db)):
    if activa is not None:
        tareas = db.query(models.Tarea).filter(models.Tarea.owner_id == user_id, models.Tarea.activa == activa).offset(skip).limit(limit).all()
    else:
        tareas = db.query(models.Tarea).filter(models.Tarea.owner_id == user_id).offset(skip).limit(limit).all()
    if not tareas:
        raise HTTPException(status_code=404, detail="No existen tareas para este usuario")
       
    return tareas
