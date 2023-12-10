FROM python:3.8
WORKDIR /app
COPY . /app
RUN pip install flask flask_sqlalchemy psycopg2 python-dotenv
CMD ["python3", "management.py"]
