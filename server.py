import requests
from bs4 import BeautifulSoup

# Dictionary yang berisi URL proxy untuk setiap negara
proxy_urls = {
    'US': 'https://www.sslproxies.org/',  # Proxy untuk Amerika Serikat
    'GB': 'https://free-proxy-list.net/uk-proxy.html',  # Proxy untuk Inggris
    'CA': 'https://www.proxy-list.download/Canada',  # Proxy untuk Kanada
    'DE': 'https://www.proxy-list.download/Germany',  # Proxy untuk Jerman
    'FR': 'https://www.proxy-list.download/France',  # Proxy untuk Prancis
    'JP': 'https://www.proxy-list.download/Japan',  # Proxy untuk Jepang
    # Tambahkan negara lainnya di sini...
}

# Fungsi untuk mengambil proxy dari halaman proxy tertentu
def get_proxies(url):
    proxies = []
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Menyaring proxy yang ditampilkan di halaman
    for row in soup.find_all('tr'):
        cols = row.find_all('td')
        if len(cols) > 1:
            ip = cols[0].text.strip()
            port = cols[1].text.strip()
            proxies.append(f"{ip}:{port}")
    return proxies

# Fungsi untuk memeriksa apakah proxy berfungsi
def test_proxy(proxy):
    url = 'https://httpbin.org/ip'  # Halaman untuk memeriksa IP
    try:
        proxies = {
            "http": f"http://{proxy}",
            "https": f"http://{proxy}"
        }
        response = requests.get(url, proxies=proxies, timeout=5)
        if response.status_code == 200:
            return True
        return False
    except requests.RequestException:
        return False

# Fungsi untuk menguji dan menyimpan proxy ke satu file
def save_proxies_to_single_file():
    with open('good.txt', 'w') as good_file, open('bad.txt', 'w') as bad_file:
        for country, url in proxy_urls.items():
            print(f"Fetching proxies for {country} from {url}...")

            # Ambil proxy dari URL berdasarkan negara
            proxies = get_proxies(url)

            # Uji setiap proxy dan simpan ke file yang sesuai
            for proxy in proxies:
                print(f"Testing Proxy: {proxy}")
                if test_proxy(proxy):
                    good_file.write(f"{proxy}\n")
                    print(f"Proxy {proxy} is working.")
                else:
                    bad_file.write(f"{proxy}\n")
                    print(f"Proxy {proxy} is not working.")

# Menjalankan fungsi untuk mengambil dan menyimpan proxy ke satu file
save_proxies_to_single_file()
