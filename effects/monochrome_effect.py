import cv2

def convert_to_grayscale(input_path, output_path):
    """
    Mengubah gambar berwarna menjadi hitam-putih (monochrome) untuk efek artistik.
    
    Args:
        input_path (str): Lokasi file gambar yang akan diubah (misalnya, 'foto.jpg').
        output_path (str): Lokasi untuk menyimpan hasil gambar hitam-putih.
    
    Returns:
        str: Lokasi file hasil (output_path).
    
    Raises:
        ValueError: Jika gambar gagal dimuat (misalnya, file rusak atau tidak ada).
    """
    # Membaca gambar dari lokasi yang diberikan
    image = cv2.imread(input_path)
    
    # Memeriksa apakah gambar berhasil dimuat
    if image is None:
        raise ValueError("Gagal memuat gambar. Pastikan file ada dan tidak rusak.")
    
    # Mengubah gambar berwarna menjadi hitam-putih
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Mengubah kembali ke format warna agar kompatibel dengan efek lain
    gray_image = cv2.cvtColor(gray_image, cv2.COLOR_GRAY2BGR)
    
    # Menyimpan hasil gambar hitam-putih ke lokasi yang ditentukan
    cv2.imwrite(output_path, gray_image)
    
    # Mengembalikan lokasi file hasil
    return output_path