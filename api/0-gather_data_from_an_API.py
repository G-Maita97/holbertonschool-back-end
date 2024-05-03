#!/usr/bin/python3

import requests
import sys

# URLs de los endpoints
url_names = 'https://jsonplaceholder.typicode.com/users'
url_tasks = 'https://jsonplaceholder.typicode.com/todos'

# Verificar si se proporciona un argumento (ID de usuario) la líne de comand
if len(sys.argv) < 2:
    print("Usage: python3 0-gather_data_from_an_API.py <user_id>")
    sys.exit(1)

# Obtener el ID de usuario desde el primer argumento de la línea de comandos
user_id = int(sys.argv[1])

# Realizar la solicitud a url_names para obtener los datos de usuarios
response_names = requests.get(url_names)

# Verificar el estado de la response_names
if response_names.status_code == 200:
    users_data = response_names.json()
else:
    rn_s = response_names.status_code
    print(f'Error al obtener datos de usuarios. Código de estado: {rn_s}')
    sys.exit(1)  # Salir del script si hay un error

# Realizar la solicitud a url_tasks para obtener los datos de tareas
response_tasks = requests.get(url_tasks)

# Verificar el estado de la response_tasks
if response_tasks.status_code == 200:
    # Convertir la respuesta JSON en una lista de tareas
    tasks_data = response_tasks.json()
else:
    rt_s = response_tasks.status_code
    print(f'Error al obtener datos de tareas. Código de estado: {rt_s}')
    sys.exit(1)  # Salir del script si hay un error

# Crear un diccionario para mapear el ID de usuario a su nombre
user_id_to_name = {user['id']: user['name'] for user in users_data}

# Contar las tareas completadas por el usuario específico (user_id)
completed_count = 0
total_tasks = 0
for task in tasks_data:
    if task['userId'] == user_id:
        total_tasks += 1
        if task['completed']:
            completed_count += 1

# Obtener el nombre del usuario
user_name = user_id_to_name.get(user_id, 'Unknown')
# Mostrar el resumen de tareas completadas para el usuario específico
print(f"Employee {user_name} is done with tasks("
      f"{completed_count}/{total_tasks}):")
for task in tasks_data:
    if task['userId'] == user_id and task['completed']:
        print(f"    {task['title']}")
