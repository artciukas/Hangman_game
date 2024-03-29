FROM python:3.11.4
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY src/ .
CMD python3 -m unittest ; python3 run.py