# Importamos Session de SQLAlchemy para realizar las solicitudes a la base de datos
from sqlalchemy.orm import Session

# Importamos models y shcemas desde la misma carpeta
from . import models, schemas
# Función que devuelve un usuario por su ID
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

# Función que devuelve un usuario por su email
def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

# Función que devuelve los usuarios registrados
def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

# Función para crear un usuario
def create_user(db: Session, user: schemas.UserCreate):
    try:
        fake_hashed_password = user.password
        db_user = models.User(email= user.email, hashed_password=fake_hashed_password)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
    except Exception as e:
        print ("Escepción?: ", e)
    finally:
        return db_user

# Función para eliminar un usuario por su ID
def delete_user_by_id(db: Session, user_id: int):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    # Si no existe
    if user is None:
        return None
    # Si existe
    else:
        db.delete(user)
        db.commit()
        return user

# Obtener tarea por id
def get_tarea(db: Session, user_id: int, activa: bool, skip: int = 0, limit: int = 100):
    return db.query(models.Tarea).filter(models.Tarea.owner_id == user_id).offset(skip).limit(limit).first()


# Función que devuelve una lista de tareas
def get_tareas(db: Session, user_id: int, activa: bool, skip: int = 0, limit: int = 100):
    if activa:
        return db.query(models.Tarea).filter(models.Tarea.activa == True, models.Tarea.owner_id == user_id).offset(skip).limit(limit).all()
    else:
        return db.query(models.Tarea).filter(models.Tarea.activa == False, models.Tarea.owner_id == user_id).offset(skip).limit(limit).all()

# Función para crear una nueva tarea a un usuario
def create_user_tarea(db: Session, tarea: schemas.TareaCreate, user_id: int):
    db_tarea = models.Tarea(**tarea.dict(), owner_id=user_id)
    db.add(db_tarea)
    db.commit()
    db.refresh(db_tarea)
    return db_tarea
# Función para eliminar una tarea a un usuario
# POR PROBAR ---------------------------
def delete_user_tarea(db: Session, tarea_id: int, user_id: int):
    db_tarea = db.query(models.Tarea).filter(models.Tarea.id == tarea_id, models.Tarea.owner_id == user_id).first()
    if db_tarea is None:
        return None
    db.delete(db_tarea)
    db.commit()
    return db_tarea
# Función para actualizar una tarea de un usuario
# POR PROBAR -----------------------------
def update_user_tarea(db: Session, tarea_id: int, user_id: int, tarea: schemas.TareaCreate):
    db_tarea = db.query(models.Tarea).filter(models.Tarea.id == tarea_id, models.Tarea.owner_id == user_id).first()
    if db_tarea is None:
        return None
    for key, value in tarea.dict().items():
        setattr(db_tarea, key, value)
    db.commit()
    db.refresh(db_tarea)
    return db_tarea

#actualizar datos de tarea 
def update_user_tarea_estado(db: Session, tarea_id: int, tarea_update: schemas.TareaUpdate):
    db_tarea = db.query(models.Tarea).filter(models.Tarea.id == tarea_id).first()
    if db_tarea is None:
        return None
    for field, value in tarea_update.dict().items():
        setattr(db_tarea, field, value)
    db.commit()
    db.refresh(db_tarea)
    return db_tarea
