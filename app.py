from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

from sample_classify_document import classify_document

@app.route('/classify', methods=['POST'])
def classify():
    file = request.files.get('file')
    if file:
        results = classify_document(file.stream)
        print(results)  # Add this to debug
        return jsonify(results)
    else:
        return jsonify({"error": "No file uploaded"}), 400

if __name__ == "__main__":
    app.run(debug=True)
