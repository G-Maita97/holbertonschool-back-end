#!/usr/bin/python3

import json
import requests

# URLs de los endpoints
url_users = 'https://jsonplaceholder.typicode.com/users'
url_todos = 'https://jsonplaceholder.typicode.com/todos'

# Realizar la solicitud a url_users para obtener los datos de usuarios
response_users = requests.get(url_users)

# Verificar el estado de la response_users
if response_users.status_code != 200:
    print(f'Error al obtener datos de usuarios. Código de estado: '
          f'{response_users.status_code}')
    exit(1)  # Salir del script si hay un error en la solicitud de usuarios

# Convertir la respuesta JSON de usuarios en una lista de usuarios
users_data = response_users.json()

# Realizar la solicitud a url_todos para obtener los datos de tareas
response_todos = requests.get(url_todos)

# Verificar el estado de la response_todos
if response_todos.status_code != 200:
    print(f'Error al obtener datos de tareas. Código de estado: '
          f'{response_todos.status_code}')
    exit(1)  # Salir del script si hay un error en la solicitud de tareas

# Convertir la respuesta JSON de tareas en una lista de tareas
todos_data = response_todos.json()

# Crear un diccionario para almacenar todas las tareas por usuario
all_tasks = {}

# Crear un diccionario para mapear el ID de usuario a su nombre
user_id_to_name = {user['id']: user['name'] for user in users_data}

# Filtrar las tareas para cada usuario
for user in users_data:
    user_id = user['id']
    username = user['name']
    user_tasks = []

    for task in todos_data:
        if task['userId'] == user_id:
            task_info = {
                'nombre_usuario': username,
                'task': task['title'],
                'completed': task['completed']
            }
            user_tasks.append(task_info)

    all_tasks[user_id] = user_tasks

# Escribir los resultados en un archivo JSON
json_filename = 'todo_all_employees.json'
with open(json_filename, 'w') as jsonfile:
    json.dump(all_tasks, jsonfile, indent=4)

print(f"Los datos se han exportado correctamente en '{json_filename}'.")
