from flask import Flask, request, jsonify, render_template
import os
import csv
import uuid
import json
from flashcard_functions import save_flashcard, load_flashcards, process_batch_file



app = Flask(__name__)

# For testing locally will replace with s3 bucket 
LOCAL_STORAGE = "flashcards"

if not os.path.exists(LOCAL_STORAGE):
    os.makedirs(LOCAL_STORAGE)

# Home screen for the web app
@app.route("/")
def home():
    flashcards = load_flashcards(LOCAL_STORAGE)
    return render_template("flashcard.html", flashcards=flashcards)


@app.route("/flashcards", methods=["POST", "GET"])
def manage_flashcards():
    if request.method == "GET":
        flashcards = load_flashcards(LOCAL_STORAGE)
        return jsonify({"flashcards": flashcards})

    if request.method == "POST":
        data = request.get_json()
        if not data.get("word") or not data.get("translation"):
            return jsonify({"error": "Both 'word' and 'translation' are required."}), 400

        word_id = str(uuid.uuid4())
        flashcard = {
            "id": word_id,
            "word": data["word"],
            "translation": data["translation"],
            "examples": data.get("examples", [])
        }
        save_flashcard(flashcard, LOCAL_STORAGE)
        return jsonify({"message": "Flashcard created successfully.", "flashcard": flashcard})


@app.route("/flashcards/batch", methods=["POST"])
def batch_flashcards():
    if "file" not in request.files:
        return jsonify({"error": "No file provided."}), 400

    file = request.files["file"]
    if not file.filename.endswith(".csv"):
        return jsonify({"error": "Only CSV files are allowed."}), 400

    result = process_batch_file(file, LOCAL_STORAGE)
    return jsonify({"message": f"{result['processed']} flashcards processed successfully.",
                    "errors": result["errors"]})


if __name__ == "__main__":
    app.run(debug=True)