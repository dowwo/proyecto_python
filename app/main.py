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
@app.post("/crear_usuario/", response_model=schemas.User)
# Recibe un email
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    # Si ya existe el email
    if db_user:
        # Arroja una HTTPException con código 400 y el detalle, emial ya registrado
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)

# Respuesta a una solicitud GET que devuelve los usuarios registrados
@app.get("/ver_usuarios/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

# Respuesta que devuelve una consulta de usuario por su id de usuario
@app.get("/buscar_usuario/{user_id}", response_model=schemas.User)
# Esta función recibe un id de usuario en la URL
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    # Si no existe
    if db_user is None:
        # Arroja una HTTPException con código 404
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return db_user

# Respuesta a la petición para modificar un usuario
@app.put("/actualizar_usuario/{user_id}", response_model=schemas.UserUpdate)
def update_user(user_id: int, user_update: schemas.UserUpdate, db: Session = Depends(get_db)):
    db_user = crud.update_user(db, user_id, user_update)
    if db_user is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return db_user

# endpoint DELETE para eliminar un usuario pasando su id en la URL
@app.delete("/eliminar_usuario/{user_id}", response_model=schemas.UserDelete)
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
@app.post("/crear_tareas/", response_model=schemas.Tarea)
def create_tarea(tarea: schemas.TareaCreate, user_id: int, db: Session = Depends(get_db)):
    db_tarea = models.Tarea(**tarea.dict(), owner_id=user_id)
    db.add(db_tarea)
    db.commit()
    db.refresh(db_tarea)
    return db_tarea
    
# Respuesta a la solicitud GET para listar todas las tareas
@app.get("/ver_tareas/", response_model=List[schemas.Tarea])
def read_tareas(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    # ESTE DEVUELVE EN FALSE LO QUE DEBE SER TRUE
    tareas = crud.get_tareas(db, skip=skip, limit=limit)
    return tareas

# Respuesta a solicitud GET para mostrar tareas por True o False
# ESTA ES LA ANTERIOR
# @app.get("/tareas/{user_id}")
# async def read_tareas(user_id: int, activa: bool = False, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     if activa:
#         # Cambiar esto para que la respuesta la retorne desde el crud
#         return db.query(models.Tarea).filter(models.Tarea.activa == True, models.Tarea.owner_id == user_id).offset(skip).limit(limit).all()
#     else:
#         return db.query(models.Tarea).filter(models.Tarea.activa == False, models.Tarea.owner_id == user_id).offset(skip).limit(limit).all()

# Respuesta a solicitud GET para mostrar tareas por True o False
@app.get("/buscar_tareas/{user_id}")
def read_tareas(user_id: int, activa: bool,db: Session = Depends(get_db)):
    db_tarea = crud.get_tareas(db, user_id, activa)
    if db_tarea is None:
        return HTTPException(status_code=404, detail="Tarea no encontrada")
    return db_tarea

# endpoint PUT para actualizar el estado de una tarea
@app.put("/actualizar_estado_tarea/{tarea_id}", response_model=schemas.Tarea)
def update_estado_tarea(tarea_id: int, tarea_update: schemas.TareaUpdateEstado, db: Session = Depends(get_db)):
    db_tarea = crud.update_user_tarea_estado(db, tarea_id, tarea_update)
    if db_tarea is None:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    return db_tarea

# SIN PROBAR SI FUNCIONAMIENTO AUN
@app.put("/modificar_tarea/{tarea_id}", response_model=schemas.Tarea)
def update_tarea(tarea_id: int, tarea_update: schemas.TareaBase, db: Session = Depends(get_db)):
    db_tarea = crud.update_user_tarea(db, tarea_id, tarea_update)
    if db_tarea is None:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    return db_tarea
        
# endpoint DELETE para eliminar una tarea pasando su id en la URL
@app.delete("/eliminar_tarea/{tarea_id}", response_model=schemas.TareaDelete)
# Se pasa el id de la tarea en la URL
def delete_tarea(tarea_id: int, db: Session = Depends(get_db)):
    db_tarea = crud.get_tarea_by_id(db, tarea_id=tarea_id)
    # Si la tarea no existe
    if db_tarea is None:
        # Arroja una HTTPException con código 404
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    crud.delete_tarea_by_id(db=db, tarea_id=tarea_id)
    return {"detail": "Tarea eliminada correctamente"}
