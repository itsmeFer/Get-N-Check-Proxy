import requests
import random
from bs4 import BeautifulSoup

# URL sumber proxy (satu halaman yang berisi berbagai proxy global)
proxy_url = 'https://www.sslproxies.org/'

# Fungsi untuk memilih bahasa
def pilih_bahasa():
    print("Pilih bahasa / Choose language:")
    print("1. Bahasa Indonesia")
    print("2. English")
    pilihan = input("Masukkan pilihan Anda / Enter your choice: ")
    if pilihan == '1':
        return "ID"
    elif pilihan == '2':
        return "EN"
    else:
        print("Pilihan tidak valid. Menggunakan bahasa Inggris sebagai default.")
        return "EN"

# Fungsi untuk mengambil proxy dari halaman
def ambil_proxies(url, lang):
    proxies = []
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    for row in soup.find_all('tr'):
        cols = row.find_all('td')
        if len(cols) > 1:
            ip = cols[0].text.strip()
            port = cols[1].text.strip()
            proxies.append(f"{ip}:{port}")
    
    if lang == "ID":
        print("Proxy berhasil diambil.")
    else:
        print("Proxies successfully retrieved.")
        
    return proxies

# Fungsi untuk memilih proxy acak
def pilih_proxy_acak(proxies_aktif):
    return random.choice(proxies_aktif)

# Fungsi untuk menguji apakah proxy berfungsi
def uji_proxy(proxy, lang):
    test_url = 'https://httpbin.org/ip'
    proxies = {
        "http": f"http://{proxy}",
        "https": f"http://{proxy}"
    }
    try:
        response = requests.get(test_url, proxies=proxies, timeout=5)
        if response.status_code == 200:
            if lang == "ID":
                print(f"Proxy {proxy} aktif.")
            else:
                print(f"Proxy {proxy} is active.")
            return True
    except requests.RequestException:
        pass
    if lang == "ID":
        print(f"Proxy {proxy} tidak aktif.")
    else:
        print(f"Proxy {proxy} is inactive.")
    return False

# Fungsi untuk menguji dan menyimpan proxy yang aktif
def ambil_dan_filter_proxies(lang):
    proxies_aktif = []
    if lang == "ID":
        print("Mengambil proxy dari:", proxy_url)
    else:
        print("Fetching proxies from:", proxy_url)
        
    proxies = ambil_proxies(proxy_url, lang)

    # Uji setiap proxy dan simpan yang berfungsi
    for proxy in proxies:
        if lang == "ID":
            print(f"Sedang Menguji Proxy: {proxy}")
        else:
            print(f"Testing Proxy: {proxy}")
            
        if uji_proxy(proxy, lang):
            proxies_aktif.append(proxy)
    return proxies_aktif

# Fungsi utama untuk melakukan permintaan menggunakan rotasi proxy
def buat_permintaan_dengan_rotasi_proxy(url, proxies_aktif, lang):
    while True:
        proxy = pilih_proxy_acak(proxies_aktif)
        
        if lang == "ID":
            print(f"Menggunakan proxy: {proxy}")
        else:
            print(f"Using proxy: {proxy}")
            
        proxies = {
            "http": f"http://{proxy}",
            "https": f"http://{proxy}"
        }
        try:
            response = requests.get(url, proxies=proxies, timeout=5)
            if response.status_code == 200:
                if lang == "ID":
                    print("Permintaan berhasil!")
                else:
                    print("Request successful!")
                return response.text
        except requests.RequestException:
            if lang == "ID":
                print(f"Proxy {proxy} gagal. Sedang mengganti proxy...\n")
            else:
                print(f"Proxy {proxy} failed. Switching proxy...\n")
                
            proxies_aktif.remove(proxy)
            if not proxies_aktif:
                if lang == "ID":
                    print("Maaf, Tidak ada proxy yang aktif.")
                else:
                    print("Sorry, No active proxies available.")
                return None

# Menjalankan program
bahasa = pilih_bahasa()
proxies_aktif = ambil_dan_filter_proxies(bahasa)
target_url = 'https://httpbin.org/ip'  # Ganti dengan URL yang diinginkan

# Membuat permintaan dengan rotasi proxy otomatis
if proxies_aktif:
    buat_permintaan_dengan_rotasi_proxy(target_url, proxies_aktif, bahasa)
else:
    if bahasa == "ID":
        print("Maaf, Tidak ada proxy yang aktif ditemukan.")
    else:
        print("Sorry, No active proxies found.")
