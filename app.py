import os
import tempfile
from google.cloud import storage
from PIL import Image
import logging

def process_image(data, context):
    bucket_name = data['bucket']
    file_name = data['name']

    if 'processed-' in file_name:
        logging.info(f"Ignoring already processed file: {file_name}")
        return

    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(file_name)
    _, temp_local_filename = tempfile.mkstemp()
    blob.download_to_filename(temp_local_filename)

    # Extract file extension
    _, file_extension = os.path.splitext(file_name)
    if not file_extension:
        logging.error(f"File {file_name} has no extension. Cannot process.")
        return

    # Convert and save the image
    img = Image.open(temp_local_filename).convert('L')
    processed_file_name = f"processed-{file_name}"
    _, temp_processed_filename = tempfile.mkstemp(suffix=file_extension)
    img.save(temp_processed_filename)

    # Upload the processed file
    processed_blob = bucket.blob(processed_file_name)
    processed_blob.upload_from_filename(temp_processed_filename)

    logging.info(f"Processed file: {processed_file_name}")
