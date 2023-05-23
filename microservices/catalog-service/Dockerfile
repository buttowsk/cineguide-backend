FROM python:3.11-alpine

ENV PYTHONUNBUFFERED=1

WORKDIR /catalogs

RUN python -m venv venv

ENV PATH="/venv/bin:$PATH"

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8083

CMD ["python", "manage.py", "runserver", "0.0.0.0:8083"]

RUN rm -rf /root/.cache