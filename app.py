from flask import Flask, render_template, request, jsonify
import os
from pddikti_lib import PddiktiLib
from lens_lib import LensLib

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Inisialisasi Library
pddikti = PddiktiLib()
lens = LensLib()

@app.route('/')
def index():
    return render_template('index.html')

# --- API PDDIKTI ---
@app.route('/api/pddikti/search', methods=['POST'])
def pddikti_search():
    keyword = request.form.get('keyword')
    result = pddikti.search(keyword)
    return jsonify(result)

@app.route('/api/pddikti/detail', methods=['POST'])
def pddikti_detail():
    id_unik = request.form.get('id')
    kategori = request.form.get('type')
    result = pddikti.get_detail(id_unik, kategori)
    return jsonify(result)

# --- API LENS SCRAPER ---
@app.route('/api/lens/scan', methods=['POST'])
def lens_scan():
    mode = request.form.get('mode') # 'url' atau 'file'
    
    if mode == 'url':
        target = request.form.get('url')
        results = lens.scan('url', target)
    
    elif mode == 'file':
        if 'file' not in request.files:
            return jsonify({"error": "No file uploaded"})
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "No file selected"})
            
        # Simpan file sementara di server
        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        # Ubah jadi absolute path (wajib buat Selenium)
        abs_path = os.path.abspath(filepath)
        file.save(abs_path)
        
        # Jalankan scan dengan path file lokal
        results = lens.scan('file', abs_path)
    
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True, port=5000)