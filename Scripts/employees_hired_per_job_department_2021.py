import pandas as pd
import requests

# URL del endpoint de la API
endpoint = 'http://localhost:5000/employees_hired_per_job_department_2021'

# Realizar solicitud GET al endpoint de la API
response = requests.get(endpoint)

# Verificar si la solicitud fue exitosa
if response.status_code == 200:
    # Parsear los datos JSON
    data = response.json()
    
    # Crear un DataFrame a partir de los datos
    df = pd.DataFrame(data)
    
    # Escribir el DataFrame en un archivo Excel
    df.to_excel('../Files/Output/employees_hired_per_job_department_2021.xlsx', index=False)
    
    print("Archivo Excel creado exitosamente.")
else:
    print("Error al obtener datos de la API.")
