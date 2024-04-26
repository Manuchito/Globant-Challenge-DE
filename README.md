# Globant-Challenge-DE
 
This is my resolution for the Globant Data Engineer Position Challenge.

## Architecture

The REST API was developed using the following tech stack:

- Pyhon
- Flask
- SQLite

## Scripts

Explanation of the scripts

- ./start.bat : Starts the whole program doing the proper exec of ./Scripts/automated_ing.bat and ./Scripts/main.py
- ./Scripts/automated_ing.bat: Has all the automatication for ingesting csv files
- ./Scripts/database_globant.py: Has the proper function to interact with the DB
- ./Scripts/departments_with_more_employees_tan_mean_2021.bat: Runs the corresponding .py file
- ./Scripts/employees_hired_per_job_departement_2021.bat: Runs the corresponding .py file
- ./Scripts/main.py: Has the whole API REST developed inside (POST / GET)

## How to use it

Run the ./start.bat file. (Make sure you have the proper libraries installed)
![image](https://github.com/Manuchito/Globant-Challenge-DE/assets/85358562/a795d362-62c4-45bd-97b1-bba543c8d7f2)

It will open two CMDs. The one on the left is the API and the other one is the "data ingestion manager"

To ingest a CSV file, you will have to move it to the /Files/Input folder. Every 5 seconds the data ingestion manager will check if there is any file there. If there is, it will try to ingest it.
It may ocurr that the file does not have the proper extension or data. Don't worry it will print a message, and save the error on a log file, located at /Files/Output/log_files.txt
![image](https://github.com/Manuchito/Globant-Challenge-DE/assets/85358562/4fa27cc0-69fc-4d45-9606-28a603082001)

Now that you have the 3 files ingested, you can extract a CSV file with the metrics needed. In order to do this, you have to run the proper .bat files for each file needed:
- ./Scripts/departments_with_more_employees_tan_mean_2021.bat
- ./Scripts/employees_hired_per_job_departement_2021.bat

If no errors were to show, then the final output will be located at /Files/Output/*.csv






 
