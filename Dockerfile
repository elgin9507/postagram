FROM python:3.12.9-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DIRPATH=/var/postagram

WORKDIR $DIRPATH

RUN apt-get update && apt-get install python3-dev default-libmysqlclient-dev build-essential pkg-config -y

COPY requirements.txt $DIRPATH

RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . $DIRPATH

EXPOSE 8080

CMD ["uvicorn", "postagram.main:app", "--host", "0.0.0.0", "--port", "8080"]
