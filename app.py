# app.py
from flask import Flask, request, redirect, url_for, render_template
from google.cloud import storage
import os

app = Flask(__name__)
client = storage.Client()
bucket = client.get_bucket('my-image-processing-bucket')

@app.route('/')
def index():
    blobs = bucket.list_blobs()
    images = [blob.name for blob in blobs if not blob.name.startswith('processed-')]
    return render_template('index.html', images=images)

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    if file:
        blob = bucket.blob(file.filename)
        blob.upload_from_file(file)
    return redirect(url_for('index'))

@app.route('/processed/<filename>')
def processed(filename):
    processed_name = f"processed-{filename}"
    blob = bucket.blob(processed_name)
    url = blob.generate_signed_url(expiration=3600)
    return redirect(url)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
