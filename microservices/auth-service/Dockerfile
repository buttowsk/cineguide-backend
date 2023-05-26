FROM python:3.11-alpine

ENV PYTHONUNBUFFERED=1

WORKDIR /auth

RUN python -m venv venv

ENV PATH="/venv/bin:$PATH"

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8081

CMD ["python", "app.py"]

RUN rm -rf /root/.cache