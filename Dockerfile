FROM python:3.9

WORKDIR /app

COPY Data/ Files/ Script/ requirements.txt README.md start.bat ./

RUN pip install --no-cache-dir -r requirements.txt

CMD ["start.bat"]
