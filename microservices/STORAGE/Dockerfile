FROM python:3.11

RUN mkdir /report /api /raw

COPY requirements.txt .


RUN apt-get clean && apt-get update

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

COPY main.py /api/main.py
COPY src/ /api/src/
WORKDIR /api

EXPOSE 5000

CMD ["python3", "-m", "uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "5000"]

