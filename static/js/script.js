/*
  JavaScript untuk Sketchify: Mengatur interaksi pengguna di halaman utama.
  Menangani unggah gambar, drag-and-drop, pilihan efek, resolusi, dan tampilan hasil.
*/

// Tunggu hingga halaman selesai dimuat
document.addEventListener('DOMContentLoaded', () => {
    // Ambil elemen dari halaman
    const uploadArea = document.getElementById('upload-area');
    const fileInput = document.getElementById('file-input');
    const uploadButton = document.getElementById('upload-button');
    const resultArea = document.getElementById('result-area');
    const originalImage = document.getElementById('original-image');
    const resultImage = document.getElementById('result-image');
    const downloadLink = document.getElementById('download-link');
    const messageText = document.getElementById('message-text');
    const resolutionSelect = document.getElementById('resolution');
    const customResDiv = document.getElementById('custom-res');
    const widthInput = document.getElementById('width');
    const heightInput = document.getElementById('height');

    // Tampilkan input resolusi custom saat memilih 'custom'
    resolutionSelect.addEventListener('change', () => {
        customResDiv.classList.toggle('hidden', resolutionSelect.value !== 'custom');
    });

    // Klik tombol unggah untuk memilih file
    uploadButton.addEventListener('click', () => {
        fileInput.click();
    });

    // Tangani drag-and-drop gambar
    uploadArea.addEventListener('dragover', (e) => {
        e.preventDefault(); // Cegah browser membuka file
    });

    uploadArea.addEventListener('drop', (e) => {
        e.preventDefault();
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            processFile(files[0]);
        }
    });

    // Tangani pemilihan file dari tombol atau drag
    fileInput.addEventListener('change', () => {
        if (fileInput.files.length > 0) {
            processFile(fileInput.files[0]);
        }
    });

    // Fungsi untuk memproses file yang diunggah
    function processFile(file) {
        // Validasi tipe file (hanya gambar)
        if (!file.type.startsWith('image/')) {
            messageText.textContent = 'Harap unggah file gambar (JPEG, PNG, dll.).';
            resultArea.classList.add('hidden');
            return;
        }

        // Siapkan data untuk dikirim ke server
        const formData = new FormData();
        formData.append('file', file);
        formData.append('conversion_type', document.getElementById('conversion-type').value);
        const resolution = resolutionSelect.value;
        formData.append('resolution', resolution);

        // Validasi dan tambahkan ukuran custom jika diperlukan
        if (resolution === 'custom') {
            const width = parseInt(widthInput.value);
            const height = parseInt(heightInput.value);
            if (isNaN(width) || isNaN(height) || width <= 0 || height <= 0) {
                messageText.textContent = 'Lebar dan tinggi harus angka positif.';
                resultArea.classList.add('hidden');
                return;
            }
            formData.append('width', width);
            formData.append('height', height);
        }

        // Nonaktifkan tombol saat memproses
        uploadButton.textContent = 'Memproses...';
        uploadButton.disabled = true;
        messageText.textContent = '';

        // Kirim gambar ke server
        fetch('/upload', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                messageText.textContent = data.error;
                resultArea.classList.add('hidden');
            } else {
                originalImage.src = data.input_url;
                resultImage.src = data.output_url;
                downloadLink.href = data.download_url;
                messageText.textContent = data.message || 'Gambar berhasil diproses dengan Sketchify!';
                resultArea.classList.remove('hidden');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            messageText.textContent = 'Terjadi kesalahan saat memproses gambar.';
            resultArea.classList.add('hidden');
        })
        .finally(() => {
            // Kembalikan tombol ke semula
            uploadButton.textContent = 'Pilih File';
            uploadButton.disabled = false;
        });
    }
});