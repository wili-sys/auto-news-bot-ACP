import requests
from bs4 import BeautifulSoup

def scrape_full_news():
    url = "https://www.alcalorpolitico.com/edicion/inicio.html"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept-Language': 'es-MX,es;q=0.9'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        results = []
        
        # Extraer noticias principales (ajustado para Al Calor Político)
        news_cards = soup.select('div.noticia') or soup.select('article.noticia') or soup.select('div.card-noticia')
        
        for card in news_cards[:3]:  # Limitar a 3 noticias para prueba
            title = card.select_one('h2, h3, h4')
            content = card.select_one('p.bajada, p.resumen, div.contenido')
            
            if title:
                news_entry = f"TÍTULO: {title.text.strip()}\n"
                if content:
                    news_entry += f"CONTENIDO: {content.text.strip()}\n"
                else:
                    # Plan B: Extraer primer párrafo cercano
                    next_p = card.find_next('p')
                    if next_p:
                        news_entry += f"CONTENIDO: {next_p.text.strip()}\n"
                
                news_entry += "────────────────────"
                results.append(news_entry)
        
        return results if results else ["Error: No se encontraron noticias completas - Revisar selectores"]

    except Exception as e:
        return [f"Error técnico: {str(e)}"]

if __name__ == "__main__":
    news = scrape_full_news()
    with open("noticias.txt", "w", encoding="utf-8") as f:
        f.write("\n\n".join(news))
