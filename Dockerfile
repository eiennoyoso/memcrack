FROM 3.10.4-slim-buster

WORKDIR /app

RUN pip3 install -r requirements.txt

ENTRYPOINT ["python3", "/app/memcrack.py"]