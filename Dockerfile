FROM python:3.11

WORKDIR /app

COPY etc/requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .


CMD python main.py