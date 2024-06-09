import os
from flask import Flask, request, redirect, url_for, render_template
from google.cloud import storage

app = Flask(__name__)
storage_client = storage.Client()
bucket_name = 'my-image-processing-bucket'  # Replace with your bucket name
bucket = storage_client.bucket(bucket_name)

@app.route('/')
def index():
    """Show the upload form and list of uploaded files."""
    blobs = bucket.list_blobs()
    return render_template('index.html', blobs=blobs)

@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle the upload of a file."""
    file = request.files['file']
    if file:
        blob = bucket.blob(file.filename)
        blob.upload_from_file(file)
        return redirect(url_for('index'))
    return "No file uploaded", 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
