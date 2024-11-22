FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt


COPY app.py .
COPY flashcard_functions.py .
COPY templates/ ./templates
COPY static/ ./static
COPY flashcards/ ./flashcards

EXPOSE 5000

CMD ["python", "app.py"]
