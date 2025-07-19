FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code and the pre-trained model
COPY ./app /app/app
COPY ./src /app/src
COPY ./tests /app/tests
COPY ./data /app/data
COPY ./models /app/models

# Expose the port
EXPOSE 80

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
