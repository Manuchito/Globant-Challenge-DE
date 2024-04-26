FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt ./
COPY main.py ./
COPY database_globant.py ./
COPY Files ./Files
COPY automated_ing.bat ./

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD ["sh", "-c", "python main.py && ./automated_ing.bat"]
