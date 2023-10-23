import json
import random
 # instalar con pip install requests
from fastapi.testclient import TestClient

from .main import app
client = TestClient(app)

# Test a un endpoint del directorio raíz que devuelve un hola mundo
def test_read_main_200():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello World"}

# Test al endpoint ver_usuarios
def test_read_users_200():
    response = client.get("/ver_usuarios/")
    assert response.status_code == 200
    print(json.dumps(response.json(), indent=4))
    assert response.json()
    
# Prueba de una ruta que no existe
def test_read_users_404():
    response = client.get("/ver_usuarios/123")
    assert response.status_code == 404

# Prueba ingresando valores erróneos a la ruta, en este caso un usuario que no existe arroja un error 404 o si se ingresan mal los datos un 422
def test_read_user_error():
    response = client.get("/buscar_usuario/9999")
    assert response.status_code == 422 or response.status_code == 404

# Prueba para la respuesta JSON, debe ser igual a {"detail":"Usuario no encontrado"}
def test_read_user_not_found():
    user_id = 99999
    response = client.get(f"/buscar_usuario/{user_id}")
    assert response.json() == {"detail":"Usuario no encontrado"}

# Prueba para el endpoint que devuelve el registro de un usuario por su id
def test_read_user_200():
    user_id = 1
    response = client.get(f"/buscar_usuario/{user_id}")
    # print(json.dumps(response.json(), indent=4))
    assert response.status_code == 200
    
# Prueba para el endpoint que crea un usuario nuevo, 
def test_create_user():
    
    # Esta código tiene como función el crear un string random
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    length = 10

    random_string = ''.join(random.choice(alphabet) for i in range(length))
    # Luego guardarlo en una variable y agregarle @email.com para que los registros de email sean siempre distintos en la prueba
    email_random = random_string + "@email.com"
    # Se crean los datos para ingresar
    data = {
        "email": f"{email_random}",
        "password": "string" 
    }
    # Se pasan a la URL como parámatro de tipo json
    response = client.post("/crear_usuario/", json=data)
    assert response.status_code == 200
    assert response.json()

# Prueba para verificar que el código que revisa si el email del usuario ya existe
def test_create_user_existente():
    # En este caso el email ya debe existir en la base de datos
    # Se crean los datos
    data = {
        "email": "roggers.morales@gmail.com",
        "password": "string"
    }
    # Se envía por la URL como parámetro de tipo json
    response = client.post("/crear_usuario/", json=data)
    assert response.json() == {'detail': 'Email already registered'}

# Prueba al endpoint actualizar_usuario
def test_update_user():
    # Se preparan los datos a actualizar
    data = {
        "email": "email@actualizado.com",
        "hashed_password": "passwordactualizada"
        }
    # Se actualiza el usuario con id 3 y los datos a modificar
    response = client.put("/actualizar_usuario/3", json=data)
    assert response.status_code == 200

# Prueba para el endpoint actualizar_usuario, donde el id de usuario no exista en la base de datos
def test_update_user_inexistente():
    data = {
        "email": "email@actualizado.com",
        "hashed_password": "passwordactualizada"
        }
    # Se actualiza el usuario con un  id inexistente para generar el error
    response = client.put("/actualizar_usuario/800", json=data)
    # Se espera una respuesta igual a 404
    assert response.status_code == 404

# Prueba para el endpoint eliminar_usuario
def test_delete_user():
    # Se envía el id de usuario por la URL
    response = client.delete("/eliminar_usuario/84")
    # Se espera una respuesta con código 200
    assert response.status_code == 200
    # Se espera una respuesta en formato json: {"detail": "Usuario eliminado correctamente"}
    assert response.json() == {"detail": "Usuario eliminado correctamente"}

# Prueba para el endpoint eliminar_usuario, en la que el id de usuario no existe
def test_delete_user_inexistente():
    # Se pasa un id de usuario inexistente en la URL
    response = client.delete("/eliminar_usuario/800")
    # Se espera un error 404
    assert response.status_code == 404

# Prueba para el endpoint buscar_tareas donde las tareas estén en estado true
def test_get_tareas_true():
    # Se envían los parámetros de la siguiente forma en la URL
    # "/ENDPOINT/id?activa=true"
    response = client.get("/buscar_tareas/1?activa=true")
    # Se espera una respuesta con código 200
    assert response.status_code == 200
    # print(json.dumps(response.json(), indent=4))
    assert response.json()

# Prueba al endpoint buscar_tareas, donde el id usuario no exista
def test_get_tareas_error():
    # Se asigna un id de usuario que no existe en la base de datos
    response = client.get("/buscar_tareas/99999?activa=true")
    # Se espera una respuesta 200
    assert response.status_code == 200
    print(json.dumps(response.json(), indent=4))
    # Se espera una respuesta en formato json con una lista vacía
    assert response.json() == []

# Prueba para el endpoint buscar_tarea ingresando datos inválidos
def test_get_tarea_ingreso_de_datos_invalidos():
    # Se pasan los datos de forma incorrecta para generar el error
    response = client.get("/buscar_tareas/1?")
    # Se espera una respuesta con código 422
    assert response.status_code == 422

# Prueba para el endpoint buscar_tarea donde la tarea no exista pero si el usuario
# En este caso, el usuario con id 7 no debería tener ninguna tarea en true o false
def test_get_tarea_inexistente():
    # Se indica un id de tarea inexistente en la base de datos
    response = client.get("/buscar_tareas/7?activa=true")
    # Se espera un código 200
    assert response.status_code == 200
    # Intento de comprobar que la lista llegue vacía
    assert response.json() == []

# Prueba al endpoint buscar_tareas donde el estado de la tarea de un usuario sea false
def test_get_tareas_false():
    # 1 es el id del usuario activa=true o false dependiendo el estado de la tarea
    response = client.get("/buscar_tareas/1?activa=false")
    # Se espera un código 200
    assert response.status_code == 200
    # print(json.dumps(response.json(), indent=4))
    assert response.json()

# Prueba al endpoint crear_tareas
def test_create_tarea():
    # Se preparan los datos para crear la tarea
    data = {
        "titulo": "tarea test",
        "descripcion": "desc test tarea",
        "fecha_vencimiento": "2023-10-22",
        "activa": True
        }
    # Se pasan los datos por la URL de la siguiente forma
    # "/ENDPOINT/?user_id=id, json=data" donde data se envía como parámetro json
    response = client.post("/crear_tareas/?user_id=1", json=data)
    # Se espera un código 200
    assert response.status_code == 200
    
# Test de error de ingreso de datos erróneos
def test_create_tarea_422():
    data = {
        "titulo": "tarea test",
        "descripcion": "desc test tarea",
        "fecha_vencimiento": "2023-10-22",
        "activa": True
        }
    # Se envían los datos de forma errónea para generar el error, en este caso no pasamos el user_id
    response = client.post("/crear_tareas/", json=data)
    assert response.status_code == 422

# Prueba al endpoint modificar_tarea
def test_update_tarea():
    # Se preparan los datos para modificar en la tarea
    data = {
        "titulo": "titulo nuevo actualizado",
        "descripcion": "descripcion nueva actualizada",
        "fecha_vencimiento": "2023-10-22",
        "activa": True
        }
    # Se envían los datos pasando el id de la tarea y la data
    response = client.put("/modificar_tarea/4", json=data)
    # Se espera un código 200
    assert response.status_code == 200

# Prueba al endpoint modificar_tarea, donde el id de la tarea no exista
def test_update_tarea_inexistente():
    data = {
        "titulo": "titulo nuevo actualizado",
        "descripcion": "descripcion nueva actualizada",
        "fecha_vencimiento": "2023-10-22",
        "activa": True
        }
    # Se envía por la URL un id de tarea inexistente
    response = client.put("/modificar_tarea/800", json=data)
    assert response.status_code == 404

# Prueba al enpoint actualizar_estado_tarea
def test_update_estado_tarea():
    # Se preparan los datos, en este caso solo cambiamos de True a False el booleano "activa"
    data = {
        
        "activa": False
    }
    # Enviamos por la URL el id de la tarea y la data a actualizar
    response = client.put("/actualizar_estado_tarea/2", json=data)
    # Esperamos una respuesta con código 200
    assert response.status_code == 200

# Prueba al endpoint actualizar_estado_tarea donde el id de la tarea no exista
def test_update_estado_tarea_inexistente():
    data = {
        
        "activa": False
    }
    # Se envía un id de tarea inexistente para generar el error
    response = client.put("/actualizar_estado_tarea/800", json=data)
    # Se espera una respuesta con código 404
    assert response.status_code == 404

# Prueba al endpoint eliminar_tarea
def test_delete_tarea():
    # Se envía por la URL el id de la tarea
    response = client.delete("/eliminar_tarea/13")
    # Se espera un código 200
    assert response.status_code == 200
    # Se espera una confirmación en formato json que debe contener: {"detail": "Tarea eliminada correctamente"}
    assert response.json() == {"detail": "Tarea eliminada correctamente"}

# Prueba al endpoint eliminar_tarea, donde el id de tarea no exista
def test_delete_tarea_inexistente():
    # Eliminamos una tarea con id 800, que no existe en la base de datos
    response = client.delete("/eliminar_tarea/800")
    # Esperamos la respuesta con código 404
    assert response.status_code == 404

