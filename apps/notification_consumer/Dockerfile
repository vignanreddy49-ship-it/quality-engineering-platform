FROM python:3.12-slim
WORKDIR /app
COPY apps/notification_consumer/requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY apps /app/apps
CMD ["python", "-m", "apps.notification_consumer.consumer"]
