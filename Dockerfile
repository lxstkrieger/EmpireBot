FROM python:3.11

WORKDIR /app

<<<<<<< HEAD
COPY etc/requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .
=======
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY EmpireBot .
>>>>>>> 71aec0c (Initial commit)


CMD python main.py