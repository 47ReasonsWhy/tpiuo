FROM python:3.12.1-slim
WORKDIR /app
COPY consumer/requirements.txt .
RUN pip install -r requirements.txt
COPY consumer/consumer.py .
CMD ["python", "consumer.py"]
