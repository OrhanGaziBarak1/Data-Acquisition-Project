from flask import Flask, render_template, request, redirect, url_for, jsonify
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# Ana sayfa
@app.route('/')
def home():
    return render_template('index.html')

# Dosya seçme sayfası
@app.route('/choose')
def choose_page():
    return render_template('upload.html')

# Dosyaları yükleme sayfası
@app.route('/upload_page')
def upload_page():
    return render_template('upload_music.html')

# Dosya yükleme sayfası
@app.route('/admin_page')
def admin_page():
    return render_template('admin.html')


# Dosyaları yükleme endpoint'i
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'fileInput' not in request.files:
        return jsonify({'error': 'No file part'})

    file = request.files['fileInput']

    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    # Dosyaların yükleneceği klasörü kontrol et ve oluştur
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    # Dosyayı kaydet
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))

    # Dosya başarıyla yüklendikten sonra anasayfaya yönlendir
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)