import requests
from bs4 import BeautifulSoup
import re

def scrape_single_news():
    try:
        url = "https://www.alcalorpolitico.com/edicion/inicio.html"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept-Language': 'es-MX,es;q=0.9',
            'Referer': 'https://www.google.com/'
        }
        
        response = requests.get(url, headers=headers, timeout=25)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extraer la primera noticia encontrada
        news_item = soup.find('article') or soup.find('div', class_=re.compile(r'noticia|articulo|post|card'))
        
        if not news_item:
            return "⚠️ No se encontró ninguna noticia en la página principal"
            
        # Extraer título
        title = news_item.find(['h1', 'h2', 'h3', 'h4']) or news_item.find(attrs={'itemprop': 'headline'})
        title_text = title.get_text(strip=True) if title else "Noticia sin título"
        
        # Extraer contenido (primeros 3 párrafos relevantes)
        content = []
        for p in news_item.find_all('p')[:3]:
            text = p.get_text(' ', strip=True)
            if len(text.split()) > 5:  # Filtrar textos cortos
                content.append(f"• {text}")
        
        if not content:
            full_text = ' '.join(news_item.get_text(' ', strip=True).split()[:100])
            content = [f"• {full_text}..."]
        
        # Formatear salida
        news_output = (
            f"📌 {title_text}\n\n" +
            "\n".join(content) +
            "\n\n🔗 Fuente: Al Calor Político"
        )
        
        return news_output
        
    except Exception as e:
        return f"⛔ Error: {str(e)}"

if __name__ == "__main__":
    noticia = scrape_single_news()
    with open("noticia.txt", "w", encoding="utf-8") as f:
        f.write(noticia)
