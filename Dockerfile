FROM python:3.11.5
LABEL maintainer="erik.agayan1@gmail.com"

ENV PYTHONUNBUFFERED 1

WORKDIR online_shop/

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt -v

COPY . .

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
