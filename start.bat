@echo off

if not exist "Files\Output\log_files.txt" (
    echo file_name^|size^|http_code^|datetime^|http_desc >> "Files\Output\log_files.txt"
)

start cmd /k python Scripts/main.py

timeout /t 5

start cmd /k call Scripts/automated_ing.bat

echo Se han iniciado las tareas main.py y automated_ing.bat en consolas separadas.
