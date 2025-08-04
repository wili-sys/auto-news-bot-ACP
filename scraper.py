import requests
from bs4 import BeautifulSoup

def scrape_news():
    url = "https://www.alcalorpolitico.com/edicion/inicio.html"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Referer': 'https://www.alcalorpolitico.com'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Selectores genéricos de emergencia
        headlines = []
        
        # Opción 1: Buscar por itemprop (común en noticias)
        for h in soup.find_all(itemprop='headline'):
            headlines.append(h.text.strip())
            
        # Opción 2: Buscar cualquier h2/h3 con texto
        if not headlines:
            for h in soup.select('h2, h3'):
                if h.text.strip() and len(h.text) > 15:
                    headlines.append(h.text.strip())
        
        return headlines if headlines else ["Error: Revisar selectores manualmente"]

    except Exception as e:
        return [f"Error HTTP: {str(e)}"]

if __name__ == "__main__":
    news = scrape_news()
    with open("noticias.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(news))
