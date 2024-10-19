import requests
from bs4 import BeautifulSoup

# Fungsi untuk mengambil proxy dari halaman SSLProxies
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
        # Menyusun dictionary untuk proxy
        proxies = {
            "http": f"http://{proxy}",
            "https": f"http://{proxy}"
        }
        # Mengirim permintaan untuk memeriksa IP dengan proxy
        response = requests.get(url, proxies=proxies, timeout=5)
        if response.status_code == 200:
            print(f"Proxy {proxy} works!")
            return True
        else:
            print(f"Proxy {proxy} failed!")
            return False
    except requests.RequestException:
        print(f"Proxy {proxy} is invalid!")
        return False

# Fungsi untuk menampilkan daftar proxy dan mengujinya
def display_proxies_and_test(proxies):
    working_proxies = []
    for proxy in proxies:
        print(f"Testing Proxy: {proxy}")
        if test_proxy(proxy):
            working_proxies.append(proxy)
            print(f"Proxy {proxy} is working.\n")
        else:
            print(f"Proxy {proxy} is not working.\n")
    return working_proxies

# URL untuk scraping proxy berdasarkan negara (misalnya, SSLProxies)
url = 'https://www.sslproxies.org/'  # Ganti dengan URL proxy lainnya sesuai negara yang ingin di-scrape

# Ambil proxy dari URL
proxies = get_proxies(url)

# Tampilkan proxy yang berhasil ditemukan
print(f"\nProxy List from {url}:\n")
for proxy in proxies:
    print(proxy)

# Menguji setiap proxy apakah valid atau tidak
working_proxies = display_proxies_and_test(proxies)

# Tampilkan proxy yang valid
print("\nWorking Proxies:\n")
for proxy in working_proxies:
    print(proxy)
