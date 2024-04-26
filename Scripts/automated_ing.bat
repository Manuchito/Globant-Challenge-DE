@echo off
setlocal EnableDelayedExpansion

set "input_folder=Files\Input"

set "log_file=Files\Output\log_files.txt"

echo ADMINISTRADOR INGESTA DE ARCHIVOS

set "curl_command=curl -X POST -F "file=@%%i" -F "batch_size=500" http://127.0.0.1:5000/upload_data"

:loop
for %%i in ("%input_folder%\*") do (
    for /f "usebackq tokens=*" %%a in (`%curl_command% 2^>^&1 ^| find /v ""`) do (
        set "last_line=%%a"
    )

    set "first_three_chars=!last_line:~0,3!"

    set ""date=%%d-%%b-%%c-%%e-%%f""

    for %%F in ("%%i") do (
        set "file_name=%%~nxF"
        set "file_size=%%~zF"
    )
    
    echo !file_name!^|!file_size!^|!first_three_chars!^|!date!^|!last_line!
    echo !file_name!^|!file_size!^|!first_three_chars!^|!date!^|!last_line! >> !log_file!

    move "%%i" "Files\Output"
)

timeout /t 5 /nobreak >nul
goto loop
