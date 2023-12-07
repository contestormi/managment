FROM python:3.8
WORKDIR /app
COPY . /app
RUN pip install flask flask_sqlalchemy
EXPOSE 5001
CMD ["python", "managment.py"]
