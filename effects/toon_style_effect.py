import cv2

def convert_to_toon_style(input_path, output_path):
    """
    Mengubah gambar menjadi gaya kartun seperti animasi dengan warna halus dan garis tebal.
    
    Args:
        input_path (str): Lokasi file gambar yang akan diubah (misalnya, 'foto.jpg').
        output_path (str): Lokasi untuk menyimpan hasil gambar kartun.
    
    Returns:
        str: Lokasi file hasil (output_path).
    
    Raises:
        ValueError: Jika gambar gagal dimuat atau ada kesalahan saat memproses.
    """
    # Membaca gambar dari lokasi yang diberikan
    img = cv2.imread(input_path)
    
    # Memeriksa apakah gambar berhasil dimuat
    if img is None:
        raise ValueError(f"Gagal memuat gambar. Pastikan file ada dan tidak rusak: {input_path}")
    
    # Mengubah gambar ke hitam-putih untuk membuat garis kartun
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Menghaluskan gambar hitam-putih agar garis lebih rapi
    gray = cv2.medianBlur(gray, 5)
    
    # Membuat garis tebal untuk gaya kartun
    edges = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 2)
    
    # Menghaluskan warna gambar asli agar terlihat seperti kartun
    color = cv2.bilateralFilter(img, 9, 75, 75)
    
    # Menggabungkan warna halus dengan garis tebal untuk efek kartun
    cartoon = cv2.bitwise_and(color, color, mask=edges)
    
    # Menyimpan hasil gambar kartun ke lokasi yang ditentukan
    cv2.imwrite(output_path, cartoon)
    
    # Mengembalikan lokasi file hasil
    return output_path