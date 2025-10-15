from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'uploads')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    domain = request.form.get('domain', 'default')
    domain_folder = os.path.join(UPLOAD_FOLDER, domain)
    os.makedirs(domain_folder, exist_ok=True)
    
    file.save(os.path.join(domain_folder, file.filename))
    return jsonify({'message': 'File uploaded successfully'})

@app.route('/files/<domain>', methods=['GET'])
def list_files(domain):
    domain_folder = os.path.join(UPLOAD_FOLDER, domain)
    if not os.path.exists(domain_folder):
        return jsonify({'files': []})
    
    files = [f for f in os.listdir(domain_folder) if os.path.isfile(os.path.join(domain_folder, f))]
    return jsonify({'files': files})

@app.route('/files/<domain>/<filename>', methods=['DELETE'])
def delete_file(domain, filename):
    file_path = os.path.join(UPLOAD_FOLDER, domain, filename)
    if os.path.exists(file_path):
        os.remove(file_path)
        return jsonify({'message': 'File deleted successfully'})
    return jsonify({'error': 'File not found'}), 404

@app.route('/files/<domain>', methods=['DELETE'])
def clear_domain_files(domain):
    domain_folder = os.path.join(UPLOAD_FOLDER, domain)
    if os.path.exists(domain_folder):
        for filename in os.listdir(domain_folder):
            file_path = os.path.join(domain_folder, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)
        return jsonify({'message': f'All files cleared for {domain}'})
    return jsonify({'message': f'No files found for {domain}'}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)