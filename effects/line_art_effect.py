import cv2
import numpy as np

def convert_to_line_art(input_path, output_path, low_threshold=100, high_threshold=200):
    """
    Mengubah gambar menjadi gambar garis seni (line art) yang menonjolkan garis tepi.
    
    Args:
        input_path (str): Lokasi file gambar yang akan diubah (misalnya, 'foto.jpg').
        output_path (str): Lokasi untuk menyimpan hasil gambar garis seni.
        low_threshold (int): Nilai minimum untuk mendeteksi garis (default: 100).
        high_threshold (int): Nilai maksimum untuk mendeteksi garis (default: 200).
    
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
        
        # Mengubah gambar berwarna menjadi hitam-putih untuk memudahkan deteksi garis
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Membuat garis seni dengan menonjolkan tepi gambar
        edges = cv2.Canny(gray, low_threshold, high_threshold)
        
        # Mengubah kembali ke format warna agar cocok dengan efek lain
        edges_bgr = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
        
        # Menyimpan hasil gambar garis seni ke lokasi yang ditentukan
        cv2.imwrite(output_path, edges_bgr)
        
        # Mengembalikan lokasi file hasil
        return output_path
    except Exception as e:
        raise ValueError(f"Kesalahan saat membuat garis seni: {str(e)}")