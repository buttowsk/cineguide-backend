FROM python:latest

WORKDIR /app

ADD . /app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "8000"]