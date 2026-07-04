FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# seed teh database
RUN python scripts/seed_data.py

EXPOSE 5000

ENV FLASK_APP=api/app.py

CMD ["python", "api/app.py"]
