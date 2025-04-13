import cv2
import numpy as np

def convert_to_art_sketch(input_path, output_path):
    """
    Mengubah gambar menjadi gaya sketsa seni dengan garis lembut dan detail halus.
    
    Args:
        input_path (str): Lokasi file gambar yang akan diubah (misalnya, 'foto.jpg').
        output_path (str): Lokasi untuk menyimpan hasil gambar sketsa.
    
    Returns:
        str: Lokasi file hasil (output_path).
    
    Raises:
        ValueError: Jika gambar gagal dimuat atau ada kesalahan saat memproses.
    """
    try:
        # Membaca gambar dari lokasi yang diberikan
        image = cv2.imread(input_path)
        
        # Memeriksa apakah gambar berhasil dimuat
        if image is None:
            raise ValueError("Gagal memuat gambar. Pastikan file ada dan tidak rusak.")
        
        # Mengubah gambar ke hitam-putih untuk mempersiapkan sketsa
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Menghaluskan gambar untuk membuat garis lebih rapi
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        
        # Membuat garis sketsa dengan menonjolkan tepi
        sobelx = cv2.Sobel(blurred, cv2.CV_64F, 1, 0, ksize=3)
        sobely = cv2.Sobel(blurred, cv2.CV_64F, 0, 1, ksize=3)
        edges = np.sqrt(sobelx**2 + sobely**2)
        edges = cv2.normalize(edges, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
        
        # Membalik garis untuk memberikan efek sketsa yang terang
        inverted_edges = 255 - edges
        
        # Menggabungkan garis sketsa dengan detail gambar asli
        sketch = cv2.addWeighted(inverted_edges, 0.8, gray, 0.2, 0)
        
        # Mengubah format untuk kompatibilitas dengan efek lain
        sketch_bgr = cv2.cvtColor(sketch, cv2.COLOR_GRAY2BGR)
        
        # Menyimpan hasil gambar sketsa ke lokasi yang ditentukan
        cv2.imwrite(output_path, sketch_bgr)
        
        # Mengembalikan lokasi file hasil
        return output_path
    except Exception as e:
        raise ValueError(f"Kesalahan saat membuat sketsa seni: {str(e)}")