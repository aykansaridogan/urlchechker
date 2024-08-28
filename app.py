from flask import Flask, request, render_template
import requests
from bs4 import BeautifulSoup
import base64

app = Flask(__name__)

# VirusTotal API Key (gizli tutun ve kodda değiştirin)
API_KEY = '2519ee5340f3778c6c50d9b6cdf52c6e9eb7cbd3e5971a5f63d367f1f3cbe7db'

def get_urls_from_page(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    urls = set(a['href'] for a in soup.find_all('a', href=True))
    return urls

def scan_url_with_virustotal(url):
    # URL'i base64 formatına dönüştürme (UTF-8 kullanarak)
    url_encoded = base64.urlsafe_b64encode(url.encode()).decode().strip("=")
    
    headers = {'x-apikey': API_KEY}
    response = requests.get(f'https://www.virustotal.com/api/v3/urls/{url_encoded}', headers=headers)
    return response.json()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        page_url = request.form['url']
        urls = get_urls_from_page(page_url)
        scan_results = {}
        for url in urls:
            scan_results[url] = scan_url_with_virustotal(url)
        return render_template('results.html', scan_results=scan_results)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
