FROM python:3.8
WORKDIR /app
COPY . /app
RUN pip install flask flask_sqlalchemy requests
EXPOSE 5002
CMD ["python", "appeals.py"]
