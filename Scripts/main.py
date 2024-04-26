import pandas as pd
import sqlite3
from database_globant import *
from flask import Flask, request, jsonify
import os

app = Flask(__name__)

FOLDER_DATA = 'Data'
FOLDER_FILES = ['Files', 'Files/Input', 'Files/Output']

@app.route('/upload_data', methods=['POST'])
def upload_csv():
    if 'file' not in request.files:
        return 'No se ha enviado ningún archivo', 400

    csv_file = request.files['file']

    if csv_file.filename == '' or csv_file.filename not in DATABASE_SCHEMA:
        return '400 : Archivo con el nombre y extension inadecuada', 400
    
    columns = DATABASE_SCHEMA[csv_file.filename]

    if csv_file and csv_file.filename.endswith('.csv'):
        
        df = pd.read_csv(csv_file, header=None, names=columns)
        batch_size = int(request.form.get('batch_size', 1000))
        print(f"Tamaño del lote: {batch_size}")  
        success, error_message = merge_data(df, csv_file.filename, batch_size=batch_size)  
        
        if success:
            return f'200 : Archivo CSV "{csv_file.filename}" subido. Datos actualizados en la base de datos correctamente', 200
        else:
            return f'400 : Error al insertar datos: {error_message}', 400
    else:
        return '400 : El archivo debe tener extensión .csv', 400

@app.route('/get_data/<table_name>', methods=['GET'])
def get_data(table_name):
    # Verificar si la tabla existe en la base de datos
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'")
    result = c.fetchone()
    conn.close()

    if result:
        # La tabla existe, ejecutar la consulta
        query = f'SELECT * FROM {table_name}'
        result = query_database(query)
        if result:
            return jsonify(result), 200
        else:
            return f'404 :No se encontraron datos en la tabla {table_name}', 404
    else:
        # La tabla no existe, devolver un mensaje de error
        return f'404 : La tabla {table_name} no existe en la base de datos', 404

@app.route('/employees_hired_per_job_department_2021', methods=['GET'])
def get_employees_hired_per_job_department_2021():
    # Consulta para obtener el número de empleados contratados por trabajo y departamento en 2021 dividido por trimestre
    query = '''
        SELECT 
                case when departments.department is null then 'No department assigned' else departments.department end, 
		        jobs.job, 
               SUM(CASE 
                   WHEN hired_employees.datetime BETWEEN '2021-01-01' AND '2021-03-31' THEN 1 
                   ELSE 0 
               END) as Q1,
               SUM(CASE 
                   WHEN hired_employees.datetime BETWEEN '2021-04-01' AND '2021-06-30' THEN 1 
                   ELSE 0 
               END) as Q2,
               SUM(CASE 
                   WHEN hired_employees.datetime BETWEEN '2021-07-01' AND '2021-09-30' THEN 1 
                   ELSE 0 
               END) as Q3,
               SUM(CASE 
                   WHEN hired_employees.datetime BETWEEN '2021-10-01' AND '2021-12-31' THEN 1 
                   ELSE 0 
               END) as Q4
        FROM hired_employees
        LEFT JOIN departments ON hired_employees.department_id = departments.id
        LEFT JOIN jobs ON hired_employees.job_id = jobs.id
        WHERE hired_employees.datetime BETWEEN '2021-01-01' AND '2021-12-31'
        GROUP BY departments.department, jobs.job
        ORDER BY departments.department, jobs.job
    '''
    result = query_database(query)
    
    # Formatear los resultados como una lista de diccionarios
    employees_per_job_department_2021 = []
    for row in result:
        department, job, q1, q2, q3, q4 = row
        employees_per_job_department_2021.append({
            'department': department,
            'job': job,
            'Q1': q1,
            'Q2': q2,
            'Q3': q3,
            'Q4': q4
        })
    
    return jsonify(employees_per_job_department_2021), 200

@app.route('/departments_with_more_employees_than_mean_2021', methods=['GET'])
def get_departments_with_more_employees_than_mean_2021():
    # Consulta para obtener el promedio de empleados contratados en 2021 para todos los departamentos
    mean_query = '''
        SELECT AVG(num_employees) as mean_employees
        FROM (
            SELECT COUNT(id) as num_employees
            FROM hired_employees
            WHERE datetime BETWEEN '2021-01-01' AND '2021-12-31'
            GROUP BY department_id
        ) as employees_per_department
    '''
    mean_result = query_database(mean_query)
    mean_employees = mean_result[0][0] if mean_result else 0
    
    # Consulta para obtener la lista de IDs, nombres y número de empleados contratados de cada departamento que haya contratado más empleados que el promedio de empleados contratados en 2021 para todos los departamentos, ordenado por el número de empleados contratados (en orden descendente)
    query = f'''
        SELECT departments.id, departments.department, COUNT(hired_employees.id) as num_employees
        FROM departments
        LEFT JOIN hired_employees ON departments.id = hired_employees.department_id
        WHERE hired_employees.datetime BETWEEN '2021-01-01' AND '2021-12-31'
        GROUP BY departments.id, departments.department
        HAVING COUNT(hired_employees.id) > {mean_employees}
        ORDER BY num_employees DESC
    '''
    result = query_database(query)
    
    # Formatear los resultados como una lista de diccionarios
    departments_with_more_employees_than_mean_2021 = []
    for row in result:
        department_id, department_name, num_employees = row
        departments_with_more_employees_than_mean_2021.append({
            'department_id': department_id,
            'department_name': department_name,
            'num_employees': num_employees
        })
    
    return jsonify(departments_with_more_employees_than_mean_2021), 200

if __name__ == '__main__':
    create_database_structure() 

    if not os.path.exists(FOLDER_DATA):
            os.makedirs(FOLDER_DATA)
    for folder_name in FOLDER_FILES:
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
    app.run(debug=True)
