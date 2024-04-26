import sqlite3

DATABASE_SCHEMA = {
    'departments.csv': ['id', 'department'],
    'jobs.csv': ['id', 'job'],
    'hired_employees.csv': ['id', 'name', 'datetime', 'department_id', 'job_id']
}


def create_database_structure():
    conn = sqlite3.connect('Data/database.db')
    c = conn.cursor()
    
    # Crear tabla departments
    c.execute('''CREATE TABLE IF NOT EXISTS departments (
                    id INTEGER PRIMARY KEY,
                    department STRING
                )''')
    
    # Crear tabla jobs
    c.execute('''CREATE TABLE IF NOT EXISTS jobs (
                    id INTEGER PRIMARY KEY,
                    job STRING
                )''')
    
    # Crear tabla hired_employees
    c.execute('''CREATE TABLE IF NOT EXISTS hired_employees (
                    id INTEGER PRIMARY KEY,
                    name STRING,
                    datetime STRING,
                    department_id INTEGER,
                    job_id INTEGER,
                    FOREIGN KEY (department_id) REFERENCES departments(id),
                    FOREIGN KEY (job_id) REFERENCES jobs(id)
                )''')
     
    conn.commit()
    conn.close()

def merge_data(df, table_name, batch_size=1000):
    conn = sqlite3.connect('Data/database.db')
    try:
        # Dividir el DataFrame en lotes de tamaño máximo especificado
        batches = [df[i:i+batch_size] for i in range(0, len(df), batch_size)]
        batch_cnt = 1
        # Iterar sobre los lotes e insertarlos en la tabla
        for batch_df in batches:
            print("Batch {}/{} de {}".format(batch_cnt,len(batches),table_name))

            batch_df.to_sql('temp_table', conn, if_exists='replace', index=False)
            conn.execute(f'''
                INSERT OR REPLACE INTO {table_name.split(".")[0]}
                SELECT * FROM temp_table
            ''')
            conn.commit()
            batch_cnt += 1
        
        return True, None  # Éxito sin errores
    except Exception as e:
        error_message = str(e)
        return False, error_message
    finally:
        conn.close()


def query_database(query):
    conn = sqlite3.connect('Data/database.db')
    c = conn.cursor()
    c.execute(query)
    result = c.fetchall()
    conn.close()
    return result

