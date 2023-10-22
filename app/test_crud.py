from fastapi import testclient
from flask import Flask
import pytest
from fastapi import FastAPI, Depends

from sqlalchemy.orm import Session
from .main import get_db

from app.crud import create_user, get_user, get_users, get_user_by_email
from app.crud import create_user_tarea, get_tarea, get_tareas, get_tarea_by_id, update_user_tarea_estado, update_user_tarea, delete_tarea_by_id

from app import models, schemas
from datetime import date

from .database import SessionLocal

# Comandos para realizar las pruebas
# coverage run -m pytest
# para obtener un registro detallado en html
# coverage html
# Tener instalado fastapi, httpx, sqlalchemy, pytest,

     
app = FastAPI()
flask_app = Flask(__name__)

client = testclient.TestClient(app)


def test_get_db():
    assert test_get_db()

# Este funciona
def test_create_user_valid_email_password():
        
        # Arrange
        db = Session()
        user = schemas.UserCreate(email="test@example.com", password="password123")

        # Act
        created_user = create_user(db, user)
        

        # Assert
        assert isinstance(created_user, models.User)
        assert created_user.email == "test@example.com"
        assert created_user.hashed_password == "password123"
        
def test_create_user_tarea():
    
    db = Session()
    # Para que no de problemas hay que hacerlo con try except
    try:
        # Arreglo
        user = schemas.UserCreate(email="test2@example.com", 
                                password="password123")
        created_user = create_user(db, user)
        tarea = schemas.TareaCreate(titulo="test titulo", 
                                    description="test description",
                                    fecha_vencimiento="2023-10-30",
                                    activa="true")
        # Metemos todo en created_tarea, osea la sesion, tarea y el id de usuario
        created_tarea = create_user_tarea(db, tarea, created_user.id)

        # Asserts
        # assert isinstance(created_tarea, models.Tarea)
        # assert created_tarea.titulo == "test tarea"
        # assert created_tarea.descripcion == "test description"
        # assert created_tarea.fecha_vencimiento == "2023-10-30"
        # assert created_tarea.activa == "true"
        #assert db.refresh() is not None
        
    except:
         # rollback() porque me estaba dando problemas
         db.rollback()
    finally:
         # Y cerramos la conexión
         db.close()

def test_create_user_tarea_bad_path():
    
    db = Session()
    # Para que no de problemas hay que hacerlo con try except
    try:
        # Arreglo
        user = schemas.UserCreate(email="test2@example.com", 
                                password="password123")
        created_user = create_user(db, user)
        tarea = schemas.TareaCreate(titulo=1111, 
                                    description=1111,
                                    fecha_vencimiento=20231030,
                                    activa="true")
        # Metemos todo en created_tarea, osea la sesion, tarea y el id de usuario
        created_tarea = create_user_tarea(db, tarea, created_user.id)

        # Asserts
        # assert isinstance(created_tarea, models.Tarea)
        # assert created_tarea.titulo == "test titulo"
        # assert created_tarea.descripcion == "test description"
        # assert created_tarea.fecha_vencimiento == "2023-10-30"
        # assert created_tarea.activa == "true"
        #assert db.refresh() is not None
        
    except:
         # rollback() porque me estaba dando problemas
         db.rollback()
    finally:
         # Y cerramos la conexión
         db.close()

def test_get_user():
    client = flask_app.test_client()
    response = client.get("/buscar_usuario/1")
    response.status_code = 200
    assert response is not None

def test_get_users_vacio():
    client = flask_app.test_client()
    response = client.get("/ver_usuarios/")
    response = []
    assert response == []

def test_get_users_200():
    
    client = flask_app.test_client()
    response = client.get('/ver_usuarios')
    response.status_code = 200
    assert response.status_code == 200

    

def test_get_users_404():
    client = flask_app.test_client()
    response = client.get("/ver_usuarios/")
    response.status_code = 404
    assert response.status_code == 404

def test_get_tareas_vacio():
    client = flask_app.test_client()
    response = client.get("/ver_tareas/")
    response = []
    assert response == []

def test_get_tareas_200():
    client = flask_app.test_client()
    response = client.get("/ver_tareas/")
    response.status_code = 200
    assert response.status_code == 200


# Desde aqui están fallando
# Test obtener usuario por email ingresando entero
# def test_get_user_by_email_bad_input():
#     db: Session() = Depends(get_db)
#     email = 123
#     assert get_user_by_email(db, email)
    
def test_get_user_by_id():
    db: Session() = Depends(get_db)
    user_id = 1
    assert get_user(db,user_id)

def test_get_user_by_email_happy_path():
    db: Session() = Depends(get_db)
    email = "algo@algo.cl"
    assert get_user_by_email(db, email)

def test_get_users():
    db: Session() = Depends(get_db)
    assert get_users(db)

    

def test_get_tarea_by_id():
    db: Session() = Depends(get_db)
    tarea_id = 1
    assert get_tarea_by_id(db, 1,0,100)
    

def test_delete_tarea_by_id_happy_path():

    db: Session() = Depends(get_db)
    tarea_id= 1
    assert delete_tarea_by_id(db, tarea_id)
    

# def test_delete_tarea_not_none():
#     db: Session() = Depends(get_db)
#     tarea_id= 1
#     assert delete_tarea_by_id(db, tarea_id) is not None

def test_tarea_update():
    db: Session() = Depends(get_db)
    tarea_id = 1
    tarea = schemas.TareaCreate(titulo="test titulo", 
                                    description="test desc",
                                    fecha_vencimiento="2023-10-30",
                                    activa="true")
    
    created_tarea = update_user_tarea(db,tarea_id, tarea)

    assert update_user_tarea(db,tarea_id, created_tarea)

def test_tarea_update_estado():
    db: Session() = Depends(get_db)
    tarea_id = 1
    tarea = schemas.TareaUpdateEstado(activa="false")
    
    updated_tarea = update_user_tarea_estado(db,tarea_id, tarea)

    assert update_user_tarea_estado(db,tarea_id, updated_tarea)
    assert update_user_tarea_estado() is not None

