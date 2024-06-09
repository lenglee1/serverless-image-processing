from flask import Flask, request, redirect, url_for, render_template
from google.cloud import storage

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return 'No file part'
    file = request.files['file']
    if file.filename == '':
        return 'No selected file'

    storage_client = storage.Client()
    bucket = storage_client.bucket('my-image-processing-bucket-us-central1')
    blob = bucket.blob(file.filename)
    blob.upload_from_file(file)

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
