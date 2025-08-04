import requests
from bs4 import BeautifulSoup

def scrape_news():
    url = "https://www.alcalorpolitico.com/edicion/inicio.html"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept-Language': 'es-MX,es;q=0.9'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Nuevos selectores actualizados (Agosto 2024)
        headlines = []
        
        # 1. Buscar noticias en artículos principales
        for article in soup.find_all('article', limit=10):
            title = article.find(['h2', 'h3', 'h4'])
            if title and title.text.strip():
                headlines.append(title.text.strip())
        
        # 2. Buscar en secciones alternativas (como backup)
        if not headlines:
            for h in soup.find_all(['h2', 'h3'], class_=True, limit=15):
                if h.text.strip():
                    headlines.append(h.text.strip())
        
        return headlines if headlines else ["Error: Revisar selectores - no se capturaron titulares"]

    except Exception as e:
        return [f"Error técnico: {str(e)}"]

if __name__ == "__main__":
    news = scrape_news()
    with open("noticias.txt", "w", encoding="utf-8") as file:
        file.write("\n".join(news))
