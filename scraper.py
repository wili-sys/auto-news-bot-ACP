import requests
from bs4 import BeautifulSoup

def scrape_news():
    url = "https://www.alcalorpolitico.com/edicion/inicio.html"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extrae titulares principales (h3 con clase específica)
        headlines = soup.find_all('h3', class_=['titulo-noticia-principal', 'titulo-noticia-secundaria'])
        news_list = [h.text.strip() for h in headlines if h.text.strip()]
        
        return news_list if news_list else ["No se encontraron noticias."]
    except Exception as e:
        return [f"Error al scrapear: {str(e)}"]

if __name__ == "__main__":
    news = scrape_news()
    with open("noticias.txt", "w", encoding="utf-8") as file:
        file.write("\n".join(news))
