# Proyecto Curso Python 2023

Este es un proyecto que abarca los conocimientos adquiridos durante el desarrollo del curso. 
Se ha desarrollado en base a la rúbrica de evaluación, con los siguientes items a calificar:
- Creación de Tareas
- Visualización de Tareas
- Edición y Eliminación de Tareas
- Marcado de Tareas como Completadas
- Cobertura de Código en Pruebas



## Authors

- [@dowwo](https://www.github.com/dowwo)

⣿⡇⣿⣿⣿⠛⠁⣴⣿⡿⠿⠧⠹⠿⠘⣿⣿⣿⡇⢸⡻⣿⣿⣿⣿⣿⣿⣿

⢹⡇⣿⣿⣿⠄⣞⣯⣷⣾⣿⣿⣧⡹⡆⡀⠉⢹⡌⠐⢿⣿⣿⣿⡞⣿⣿⣿

⣾⡇⣿⣿⡇⣾⣿⣿⣿⣿⣿⣿⣿⣿⣄⢻⣦⡀⠁⢸⡌⠻⣿⣿⣿⡽⣿⣿

⡇⣿⠹⣿⡇⡟⠛⣉⠁⠉⠉⠻⡿⣿⣿⣿⣿⣿⣦⣄⡉⠂⠈⠙⢿⣿⣝⣿

⠤⢿⡄⠹⣧⣷⣸⡇⠄⠄⠲⢰⣌⣾⣿⣿⣿⣿⣿⣿⣶⣤⣤⡀⠄⠈⠻⢮

⠄⢸⣧⠄⢘⢻⣿⡇⢀⣀⠄⣸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⡀⠄⢀

⠄⠈⣿⡆⢸⣿⣿⣿⣬⣭⣴⣿⣿⣿⣿⣿⣿⣿⣯⠝⠛⠛⠙⢿⡿⠃⠄⢸

⠄⠄⢿⣿⡀⣿⣿⣿⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣿⣿⣿⣿⡾⠁⢠⡇⢀

⠄⠄⢸⣿⡇⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣏⣫⣻⡟⢀⠄⣿⣷⣾

⠄⠄⢸⣿⡇⠄⠈⠙⠿⣿⣿⣿⣮⣿⣿⣿⣿⣿⣿⣿⣿⡿⢠⠊⢀⡇⣿⣿

⠒⠤⠄⣿⡇⢀⡲⠄⠄⠈⠙⠻⢿⣿⣿⠿⠿⠟⠛⠋⠁⣰⠇⠄⢸⣿⣿⣿


## Deployment

La estructura del proyecto es la siguiente:
proyecto_python
└── app
    ├── __init__.py
    ├── crud.py
    ├── database.py
    ├── main.py
    ├── models.py
    ├── schemas.py
    └── test_main.py

Se recomienda utilizar un entorno virtual:
Para crear un entorno virtual se utiliza el siguiente comando:
python -m venv env

Para ejecutar el entorno virtual se debe navegar a la carpeta env/scripts
y ejecutar el archivo activate

Las siguientes librerias deben estar instaladas para el correcto funcionamiento del proyecto:

Instalar las librerias:
```FastAPI
    pip  install "fastapi[all]"
```
```uvicorn
    pip install "uvicorn[standard]"
```
```httpx
    pip install httpx
```
```coverage
    pip install coverage
```
```pydantic
    pip install pydantic
```
```pytest
    pip install pytest 
```
```SQLAlchemy
    pip install sqlalchemy
```

Ya con todo instalado, y usando el entorno virtual, debemos situarnos en la carpeta proyecto_python.
Desde aquí ejecutaremos los siguientes comandos:

Inicializamos el servidor:
uvicorn app.main:app --reload
Esto nos permite probar los endpoints creados con FastAPI
en la url: 127.0.0.1/8000/docs
Se mostrará una interfaz de esta forma: https://prnt.sc/PQ_bmaAr72FP

```Ejecutamos el comando coverage para realizar los test unitarios:
    coverage run -m pytest
```

```Ejecutamos el comando coverage, en este caso crearemos un registro html 
    coverage html
```

La ruta del archivo debería ser:
proyecto_python/htmlcov/index.html
Al abrirlo debería verse de la siguiente manera
https://prnt.sc/Cs4RO1VPDa1Q
