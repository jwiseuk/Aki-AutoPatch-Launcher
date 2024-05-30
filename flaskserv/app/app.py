from flask import Flask, request, send_file
import hashlib
import os

app = Flask(__name__)

# Set the directory path for uploads and downloads
APACHE_FOLDER = '/var/www/html/'

# Get allowed IPs from environment variable
ALLOWED_IPS = os.getenv('ALLOWED_IPS', '').split(',')

@app.route('/upload', methods=['POST'])
def upload_file():
    client_ip = request.remote_addr
    if client_ip in ALLOWED_IPS:
        file = request.files.get('file')
        if file:
            filename = secure_filename(file.filename)
            file_path = os.path.join(APACHE_FOLDER, filename)
            file.save(file_path)
            # Generate MD5 checksum
            md5_hash = hashlib.md5()
            with open(file_path, 'rb') as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    md5_hash.update(chunk)
            md5_file_path = os.path.join(APACHE_FOLDER, filename + '.md5')
            with open(md5_file_path, 'w') as f:
                f.write(md5_hash.hexdigest())
            return 'File uploaded successfully.', 200
        else:
            return 'No file uploaded.', 400
    else:
        return 'Access denied. Your IP is not whitelisted.', 403

@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    file_path = os.path.join(APACHE_FOLDER, filename)
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    else:
        return 'File not found.', 404

if __name__ == '__main__':
    # Run Flask app on port 5000
    app.run(host='0.0.0.0', port=5000)