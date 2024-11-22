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


@app.route('/flashcards/<flashcard_id>', methods=['PUT'])
def update_flashcard(flashcard_id):
    try:
        # Load existing flashcards
        flashcards = load_flashcards(LOCAL_STORAGE)
        
        # Check if the flashcard exists
        flashcard = next((fc for fc in flashcards if fc["id"] == flashcard_id), None)
        if not flashcard:
            return jsonify({"error": "Flashcard not found"}), 404

        # Get updated data from the request
        data = request.get_json()
        word = data.get("word", flashcard["word"])  # Default to existing value
        translation = data.get("translation", flashcard["translation"])
        examples = data.get("examples", flashcard["examples"])

        # Update the flashcard
        flashcard["word"] = word
        flashcard["translation"] = translation
        flashcard["examples"] = examples

        # Save updated flashcards
        save_flashcard(flashcard, LOCAL_STORAGE)

        return jsonify({
            "message": "Flashcard updated successfully.",
            "flashcard": flashcard
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/flashcards/batch", methods=["POST"])
def batch_flashcards():
    if "file" not in request.files:
        return jsonify({"error": "No file provided."}), 400

    file = request.files["file"]
    if not file.filename.endswith(".csv"):
        return jsonify({"error": "Only CSV files are allowed."}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file selected."}), 400

    result = process_batch_file(file, LOCAL_STORAGE)
    return jsonify({"message": f"{result['processed']} flashcards processed successfully.",
                    "errors": result["errors"]})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)