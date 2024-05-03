#!/usr/bin/python3

import json
import requests
import sys

# URLs de los endpoints
url_names = 'https://jsonplaceholder.typicode.com/users'
url_tasks = 'https://jsonplaceholder.typicode.com/todos'

# Verificar si se proporciona un argumento(ID de usuario)en la líne de comand
if len(sys.argv) < 2:
    print("Usage: python3 2-export_to_JSON.py <user_id>")
    sys.exit(1)

# Obtener el ID de usuario desde el primer argumento de la línea de comandos
user_id = int(sys.argv[1])

# Realizar la solicitud a url_names para obtener los datos de usuarios
response_names = requests.get(url_names)

# Verificar el estado de la response_names
if response_names.status_code == 200:
    # Convertir la respuesta JSON en una lista de usuarios
    users_data = response_names.json()
else:
    st_cd_nm = response_names.status_code
    print(f'Error al obtener datos de usuarios. Código de estado: {st_cd_nm}')
    sys.exit(1)  # Salir del script si hay un error

# Realizar la solicitud a url_tasks para obtener los datos de tareas
response_tasks = requests.get(url_tasks)

# Verificar el estado de la response_tasks
if response_tasks.status_code == 200:
    # Convertir la respuesta JSON en una lista de tareas
    tasks_data = response_tasks.json()
else:
    st_cd_tk = response_tasks.status_code
    print(f'Error al obtener datos de tareas. Código de estado: {st_cd_tk}')
    sys.exit(1)  # Salir del script si hay un error

# Crear un diccionario para mapear el ID de usuario a su nombre
user_id_to_name = {user['id']: user['name'] for user in users_data}

# Filtrar las tareas que pertenecen al usuario específico (user_id)
filtered_tasks = []
for task in tasks_data:
    if task['userId'] == user_id:
        task_info = {
            'task': task['title'],
            'completed': task['completed'],
            'username': user_id_to_name.get(user_id, 'Unknown')
        }
        filtered_tasks.append(task_info)

# Escribir los resultados en un archivo JSON con el nombre USER_ID.json
json_filename = f"{user_id}.json"
with open(json_filename, 'w') as jsonfile:
    json.dump({str(user_id): filtered_tasks}, jsonfile)

print(f"Los datos se han exportado correctamente en '{json_filename}'.")
