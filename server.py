import requests
import random
from bs4 import BeautifulSoup

# URL sumber proxy (satu halaman yang berisi berbagai proxy global)
proxy_url = 'https://www.sslproxies.org/'

# Fungsi untuk mengambil proxy dari halaman
def get_proxies(url):
    proxies = []
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    for row in soup.find_all('tr'):
        cols = row.find_all('td')
        if len(cols) > 1:
            ip = cols[0].text.strip()
            port = cols[1].text.strip()
            proxies.append(f"{ip}:{port}")
    return proxies

# Fungsi untuk memilih proxy acak
def get_random_proxy(working_proxies):
    return random.choice(working_proxies)

# Fungsi untuk menguji apakah proxy berfungsi
def test_proxy(proxy):
    test_url = 'https://httpbin.org/ip'
    proxies = {
        "http": f"http://{proxy}",
        "https": f"http://{proxy}"
    }
    try:
        response = requests.get(test_url, proxies=proxies, timeout=5)
        if response.status_code == 200:
            return True
    except requests.RequestException:
        pass
    return False

# Fungsi untuk menguji dan menyimpan proxy yang aktif
def fetch_and_filter_proxies():
    working_proxies = []
    print("Mengambil proxy dari:", proxy_url)
    proxies = get_proxies(proxy_url)

    # Uji setiap proxy dan simpan yang berfungsi
    for proxy in proxies:
        print(f"Menguji Proxy: {proxy}")
        if test_proxy(proxy):
            working_proxies.append(proxy)
            print(f"Proxy {proxy} aktif.")
        else:
            print(f"Proxy {proxy} tidak aktif.")
    return working_proxies

# Fungsi utama untuk melakukan permintaan menggunakan rotasi proxy
def make_request_with_rotating_proxy(url, working_proxies):
    while True:
        proxy = get_random_proxy(working_proxies)
        print(f"Menggunakan proxy: {proxy}")
        proxies = {
            "http": f"http://{proxy}",
            "https": f"http://{proxy}"
        }
        try:
            response = requests.get(url, proxies=proxies, timeout=5)
            if response.status_code == 200:
                print("Permintaan berhasil!")
                return response.text
        except requests.RequestException:
            print(f"Proxy {proxy} gagal. Mengganti proxy...\n")
            working_proxies.remove(proxy)
            if not working_proxies:
                print("Tidak ada proxy yang aktif.")
                return None

# Ambil dan uji proxy
working_proxies = fetch_and_filter_proxies()
target_url = 'https://httpbin.org/ip'  # Ganti dengan URL yang diinginkan

# Membuat permintaan dengan rotasi proxy otomatis
if working_proxies:
    make_request_with_rotating_proxy(target_url, working_proxies)
else:
    print("Tidak ada proxy yang aktif ditemukan.")
