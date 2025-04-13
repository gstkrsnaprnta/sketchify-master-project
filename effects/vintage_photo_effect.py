import cv2
import numpy as np

def convert_to_vintage_photo(input_path, output_path):
    """
    Mengubah gambar menjadi gaya foto lama dengan warna kecokelatan, bintik, dan pinggiran gelap.
    
    Args:
        input_path (str): Lokasi file gambar yang akan diubah (misalnya, 'foto.jpg').
        output_path (str): Lokasi untuk menyimpan hasil gambar vintage.
    
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
        
        # Mengubah warna gambar jadi kecokelatan seperti foto lama
        sepia_matrix = np.array([[0.272, 0.534, 0.131],
                                [0.349, 0.686, 0.168],
                                [0.393, 0.769, 0.189]])
        sepia_image = cv2.transform(image, sepia_matrix)
        sepia_image = np.clip(sepia_image, 0, 255).astype(np.uint8)
        
        # Menambahkan bintik-bintik untuk efek usang
        noise = np.random.normal(0, 25, sepia_image.shape).astype(np.uint8)
        noisy_image = cv2.add(sepia_image, noise)
        
        # Membuat pinggiran gelap untuk tampilan klasik
        rows, cols = noisy_image.shape[:2]
        kernel_x = cv2.getGaussianKernel(cols, cols / 3)
        kernel_y = cv2.getGaussianKernel(rows, rows / 3)
        kernel = kernel_y * kernel_x.T
        mask = 255 * kernel / np.linalg.norm(kernel)
        mask = mask.astype(np.uint8)
        vintage_image = noisy_image.copy()
        for i in range(3):
            vintage_image[:, :, i] = vintage_image[:, :, i] * (0.3 + 0.7 * mask / 255)
        
        # Meningkatkan kontras untuk hasil lebih tajam
        vintage_image = cv2.convertScaleAbs(vintage_image, alpha=1.2, beta=0)
        
        # Menyimpan hasil gambar vintage ke lokasi yang ditentukan
        cv2.imwrite(output_path, vintage_image)
        
        # Mengembalikan lokasi file hasil
        return output_path
    except Exception as e:
        raise ValueError(f"Kesalahan saat membuat foto vintage: {str(e)}")