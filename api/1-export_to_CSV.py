#!/usr/bin/python3

import csv
import requests
import sys

# URLs de los endpoints
url_names = 'https://jsonplaceholder.typicode.com/users'
url_tasks = 'https://jsonplaceholder.typicode.com/todos'

# Verificar si se proporciona un argumento(ID de usuario) enla líne de comand
if len(sys.argv) < 2:
    print("Usage: python3 1-export_to_CSV.py <user_id>")
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
            'User ID': user_id,
            'Username': user_id_to_name.get(user_id, 'Unknown'),
            'Task Completed Status': str(task['completed']),
            'Task Title': task['title']
        }
        filtered_tasks.append(task_info)

# Escribir los resultados en un archivo CSV con el nombre USER_ID.csv
csv_filename = f"{user_id}.csv"
with open(csv_filename, 'w', newline='') as csvfile:
    fieldnames = ['User ID', 'Username', 'Task Completed Status', 'Task Title']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for task in filtered_tasks:
        writer.writerow(task)

print(f"Los datos se han exportado correctamente en '{csv_filename}'.")
