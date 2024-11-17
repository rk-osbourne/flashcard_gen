import os
import csv
import json


def save_flashcard(flashcard, storage_dir):
    file_path = os.path.join(storage_dir, f"{flashcard['id']}.json")
    with open(file_path, "w") as f:
        json.dump(flashcard, f)


def load_flashcards(storage_dir):
    flashcards = []
    for file in os.listdir(storage_dir):
        if file.endswith(".json"):
            with open(os.path.join(storage_dir, file), "r") as f:
                flashcards.append(json.load(f))
    return flashcards


def process_batch_file(file, storage_dir):
    processed = 0
    errors = []

    reader = csv.DictReader(file.read().decode("utf-8").splitlines())
    for row in reader:
        if "word" not in row or "translation" not in row:
            errors.append(f"Missing required fields in row: {row}")
            continue

        try:
            flashcard = {
                "id": str(uuid.uuid4()),
                "word": row["word"],
                "translation": row["translation"],
                "examples": row.get("examples", "").split(";")
            }
            save_flashcard(flashcard, storage_dir)
            processed += 1
        except Exception as e:
            errors.append(f"Error processing row {row}: {str(e)}")

    return {"processed": processed, "errors": errors}
