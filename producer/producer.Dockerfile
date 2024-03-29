FROM python:3.12.1-slim
WORKDIR /app
COPY producer/requirements.txt .
RUN pip install -r requirements.txt
COPY producer/producer.py .
CMD ["python", "producer.py"]
