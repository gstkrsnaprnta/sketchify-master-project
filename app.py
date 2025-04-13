from flask import Flask, request, render_template, jsonify, send_file
import os
from time import time
import logging

# Impor fungsi efek dari modul yang sudah diperbarui
from effects.monochrome_effect import convert_to_grayscale
from effects.line_art_effect import convert_to_line_art
from effects.toon_style_effect import convert_to_toon_style  
from effects.ink_blot_effect import convert_to_ink_blot
from effects.art_sketch_effect import convert_to_art_sketch
from effects.vintage_photo_effect import convert_to_vintage_photo
from effects.resize_image import resize_image

"""
Aplikasi web Sketchify untuk mengubah gambar dengan efek seni seperti sketsa, komik, dan lukisan.
Menerima unggahan gambar, menerapkan efek, dan menyediakan hasil untuk diunduh.
"""

# Mengatur logging untuk membantu menemukan masalah
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Inisialisasi aplikasi Flask
app = Flask(__name__, static_folder='static', template_folder='templates')

# Menentukan folder untuk menyimpan gambar yang diunggah dan hasil efek
UPLOAD_FOLDER = 'static/uploads'
OUTPUT_FOLDER = 'static/outputs'

# Membuat folder jika belum ada
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Peta efek: menghubungkan jenis efek dengan fungsi yang sesuai
EFFECTS = {
    'monochrome_glow': convert_to_grayscale,
    'line_art': convert_to_line_art,
    'toon_style': convert_to_toon_style,
    'ink_blot': convert_to_ink_blot,
    'art_sketch': convert_to_art_sketch,
    'vintage_photo': convert_to_vintage_photo,
}

@app.route('/')
def index():
    """
    Menampilkan halaman utama aplikasi (index.html).
    """
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_image():
    """
    Menerima gambar yang diunggah, menerapkan efek seni, dan menghasilkan gambar hasil.
    Mengembalikan URL untuk menampilkan dan mengunduh hasil.
    """
    # Memeriksa apakah ada file dalam unggahan
    if 'file' not in request.files:
        return jsonify({'error': 'Tidak ada file yang diunggah'}), 400
    
    file = request.files['file']
    
    # Memeriksa apakah nama file tidak kosong
    if file.filename == '':
        return jsonify({'error': 'Tidak ada file yang dipilih'}), 400
    
    # Memeriksa jenis file yang diizinkan (jpg, jpeg, png)
    allowed_extensions = {'.jpg', '.jpeg', '.png'}
    if not os.path.splitext(file.filename)[1].lower() in allowed_extensions:
        return jsonify({'error': 'Jenis file tidak valid. Hanya JPG, JPEG, dan PNG yang diizinkan.'}), 400
    
    # Membuat nama file unik untuk gambar yang diunggah
    input_filename = f"input_{int(time())}_{file.filename}"
    input_path = os.path.join(UPLOAD_FOLDER, input_filename)
    
    # Mendapatkan jenis efek, resolusi, dan ukuran dari formulir
    conversion_type = request.form.get('conversion_type', 'monochrome_glow')
    resolution = request.form.get('resolution', 'original')
    width = request.form.get('width')
    height = request.form.get('height')
    
    # Membuat nama file untuk hasil efek
    output_filename = f"{conversion_type}_{int(time())}_{file.filename}"
    temp_path = os.path.join(OUTPUT_FOLDER, f"temp_{output_filename}")
    final_output_path = os.path.join(OUTPUT_FOLDER, output_filename)
    
    # Menyimpan gambar yang diunggah
    file.save(input_path)
    logging.debug(f"Gambar disimpan di: {input_path}")
    
    try:
        # Memeriksa apakah jenis efek valid
        if conversion_type not in EFFECTS:
            raise ValueError(f"Jenis efek tidak dikenal: {conversion_type}")
        
        # Menerapkan efek yang dipilih
        effect_function = EFFECTS[conversion_type]
        result_path = effect_function(input_path, temp_path)
        
        # Memeriksa apakah file sementara berhasil dibuat
        if not os.path.exists(temp_path):
            raise ValueError(f"Gagal membuat file sementara untuk efek {conversion_type}: {temp_path}")
        
        logging.debug(f"Efek {conversion_type} diterapkan, file sementara: {temp_path}")
        
        # Mengubah ukuran gambar sesuai pilihan pengguna
        resize_image(temp_path, final_output_path, resolution, width, height)  
        logging.debug(f"Gambar diubah ukurannya ke: {final_output_path}")
        
        # Menyiapkan respons dengan URL gambar
        response = {
            'message': 'Gambar selesai diproses',
            'input_url': f'/static/uploads/{input_filename}',
            'output_url': f'/static/outputs/{output_filename}',
            'download_url': f'/download?file={output_filename}'
        }
        
        # Membersihkan file sementara
        os.remove(temp_path)
        logging.debug(f"File sementara dihapus: {temp_path}")
        
        return jsonify(response)
    
    except ValueError as e:
        # Menangani kesalahan yang diketahui (misalnya, file gagal diproses)
        logging.error(f"Kesalahan: {str(e)}")
        if os.path.exists(input_path):
            os.remove(input_path)
        if os.path.exists(temp_path):
            os.remove(temp_path)
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        # Menangani kesalahan tak terduga
        logging.error(f"Kesalahan tak terduga: {str(e)}")
        if os.path.exists(input_path):
            os.remove(input_path)
        if os.path.exists(temp_path):
            os.remove(temp_path)
        return jsonify({'error': 'Terjadi kesalahan saat memproses gambar'}), 500

@app.route('/download', methods=['GET'])
def download_file():
    """
    Mengizinkan pengguna mengunduh gambar hasil efek.
    """
    # Mendapatkan nama file dari permintaan
    filename = request.args.get('file')
    file_path = os.path.join(OUTPUT_FOLDER, filename)
    
    logging.debug(f"Mengunduh file: {file_path}")
    
    # Memeriksa apakah file ada
    if not os.path.exists(file_path):
        return jsonify({'error': 'File tidak ditemukan'}), 404
    
    # Mengirim file untuk diunduh
    return send_file(file_path, as_attachment=True, download_name=filename)

if __name__ == '__main__':
    # Menjalankan aplikasi dalam mode debug
    app.run(debug=True)