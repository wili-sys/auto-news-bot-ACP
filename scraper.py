import requests
from bs4 import BeautifulSoup
import re

def scrape_full_news(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
            'Accept-Language': 'es-MX,es;q=0.9'
        }
        
        response = requests.get(url, headers=headers, timeout=25)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extraer título (ajustado para Al Calor Político)
        title = soup.find('h1', class_=re.compile(r'title|entry-title', re.I))
        title_text = title.get_text(strip=True) if title else "Noticia de Al Calor Político"
        
        # Extraer contenido principal (ajusta según la estructura real del sitio)
        content = []
        article_body = soup.find('div', class_=re.compile(r'entry-content|article-body|post-content', re.I))
        
        if article_body:
            paragraphs = article_body.find_all('p')
            for p in paragraphs:
                text = p.get_text(' ', strip=True)
                if len(text.split()) > 3:  # Filtrar párrafos vacíos
                    content.append(text)
        
        if not content:
            return None  # Fallback para manejar en main.py
        
        return {
            'title': title_text,
            'content': '\n'.join(content),
            'url': url
        }
        
    except Exception as e:
        print(f"⛔ Error en scraping: {e}")
        return None
