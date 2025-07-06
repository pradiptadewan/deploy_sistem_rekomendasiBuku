import time
import requests
from django.core.management.base import BaseCommand
from django.conf import settings
from sistem.models import Book

class Command(BaseCommand):
    """
    Perintah Django kustom untuk mengambil URL gambar sampul dari Google Books API
    dan menyimpannya ke database untuk buku yang belum memiliki gambar.
    """
    help = 'Mengambil URL gambar sampul dari Google Books API untuk buku yang belum memiliki gambar.'

    def handle(self, *args, **kwargs):
        # 1. Ambil semua buku dari database yang kolom image_url-nya masih kosong atau null.
        # Ini memastikan kita hanya bekerja pada data yang dibutuhkan.
        books_to_update = Book.objects.filter(image_url__isnull=True)

        # Jika tidak ada buku yang perlu diupdate, hentikan skrip lebih awal.
        if not books_to_update.exists():
            self.stdout.write(self.style.SUCCESS('Semua buku sudah memiliki gambar sampul.'))
            return

        self.stdout.write(self.style.NOTICE(f'Menemukan {books_to_update.count()} buku untuk diperbarui...'))

        # 2. Loop melalui setiap buku yang perlu diupdate.
        for book in books_to_update:
            try:
                # Membuat query pencarian yang lebih spesifik berdasarkan judul dan penulis.
                query = f"{book.title} {book.author}"
                api_key = settings.GOOGLE_BOOKS_API_KEY

                # Jika API Key tidak diatur, hentikan proses untuk menghindari error.
                if not api_key:
                    self.stdout.write(self.style.ERROR('GOOGLE_BOOKS_API_KEY tidak diatur di environment variables.'))
                    return

                # Alamat (endpoint) dari Google Books API.
                url = f"https://www.googleapis.com/books/v1/volumes?q={query}&key={api_key}"

                # Mengirim permintaan GET ke API.
                response = requests.get(url, timeout=10) # Tambahkan timeout untuk mencegah hang
                response.raise_for_status()  # Cek jika ada error HTTP (misal: 404, 500).

                data = response.json()

                # 3. Memeriksa dan mem-parsing data JSON yang diterima dari API.
                if 'items' in data and len(data['items']) > 0:
                    volume_info = data['items'][0]['volumeInfo']
                    # Pastikan 'imageLinks' dan 'thumbnail' ada untuk menghindari error.
                    if 'imageLinks' in volume_info and 'thumbnail' in volume_info['imageLinks']:
                        image_url = volume_info['imageLinks']['thumbnail']

                        # Simpan URL gambar ke database.
                        book.image_url = image_url
                        book.save()

                        self.stdout.write(self.style.SUCCESS(f'Berhasil menemukan sampul untuk: "{book.title}"'))
                    else:
                        self.stdout.write(self.style.WARNING(f'Tidak ada link gambar untuk: "{book.title}"'))
                else:
                    self.stdout.write(self.style.WARNING(f'Tidak ada hasil pencarian untuk: "{book.title}"'))

            except requests.exceptions.RequestException as e:
                # Menangani error jaringan secara spesifik (misal: timeout, koneksi gagal).
                self.stdout.write(self.style.ERROR(f'Error jaringan saat memproses "{book.title}": {e}'))
            except Exception as e:
                # Menangani error lainnya yang mungkin terjadi.
                self.stdout.write(self.style.ERROR(f'Error tak terduga saat memproses "{book.title}": {e}'))

            # 4. PENTING: Beri jeda 1 detik antar permintaan.
            # Ini untuk menghindari pembatasan (rate limiting) dari Google API.
            time.sleep(1)

        self.stdout.write(self.style.SUCCESS('Proses pembaruan gambar sampul selesai.'))
