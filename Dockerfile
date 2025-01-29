FROM python:3.9

WORKDIR /app

RUN pip install --upgrade pip
RUN pip install pipenv
RUN pipenv install


COPY Pipfile* /app
RUN cd /app && pipenv requirements > requirements.txt

RUN pip install -U --upgrade pip --no-cache-dir -r /app/requirements.txt

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y

COPY . /app/

# DEV
CMD ["python", "./app.py"]


