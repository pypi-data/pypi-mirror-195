import requests
from loadwave import Loader
import os
import sys

def check(url, updateurl, version):
    try:
        response = requests.get(url)
        latest_version = response.text.strip()
        if latest_version != version:
            print('Güncelleme bulundu! Mevcut sürüm:', version, 'En son sürüm:', latest_version)
            update()
        else:
            print('Programınız güncel.')
    except requests.exceptions.RequestException:
        print('Bağlantı hatası: Güncelleme kontrol edilemedi.')

def update(url):
    try:
        response = requests.get(url, stream=True)
        total_size_in_bytes = int(response.headers.get('content-length', 0))
        block_size = 1024  # 1 KB
        downloaded_size = 0
        with open('new.zip', 'wb') as file:
            loader = Loader('Downloading')
            loader.start()  # Yükleme ekranını başlat
            for data in response.iter_content(block_size):
                downloaded_size += len(data)
                file.write(data)
                status = f"\r{downloaded_size}/{total_size_in_bytes} bytes [{(downloaded_size / total_size_in_bytes) * 100:.2f}%]"
                status = status + ' ' * (len(loader.message) - len(status))
                sys.stdout.write(status)
                sys.stdout.flush()
            loader.stop()  # Yükleme ekranını durdur
        print('\nProgram güncellendi. Yeniden başlatılıyor...')
        os.execl(sys.executable, sys.executable, *sys.argv)
    except requests.exceptions.RequestException:
        print('Bağlantı hatası: Güncelleme indirilemedi.')
