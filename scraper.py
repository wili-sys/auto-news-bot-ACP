# scraper.py
import requests
from bs4 import BeautifulSoup
import re

def scrape_single_news():
    try:
        url = "https://www.alcalorpolitico.com/edicion/inicio.html"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml',
            'Accept-Language': 'es-MX,es;q=0.9',
        }
        
        response = requests.get(url, headers=headers, timeout=25)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Estrategia de búsqueda agresiva
        news_candidates = soup.find_all(['article', 'div'], class_=lambda x: x and any(word in x.lower() for word in ['noticia', 'post', 'articulo', 'card', 'principal']))
        
        if not news_candidates:
            # Plan B: Buscar cualquier contenedor con título y párrafos
            news_candidates = [elem for elem in soup.find_all(['div', 'section']) 
                             if elem.find(['h1', 'h2', 'h3']) and len(elem.find_all('p')) > 1]
        
        if not news_candidates:
            return "⚠️ Error: Estructura del sitio cambiada - Se necesitan ajustar los selectores"
            
        # Tomar la primera noticia válida
        news_item = news_candidates[0]
        
        # Extraer título
        title = (news_item.find(['h1', 'h2', 'h3']) or 
                news_item.find(attrs={'itemprop': 'headline'}) or
                news_item.find(class_=re.compile(r'titulo|title|headline', re.I)))
        title_text = title.get_text(strip=True) if title else "Última noticia"
        
        # Extraer contenido (3 párrafos principales)
        content = []
        paragraphs = news_item.find_all('p', class_=lambda x: not x or 'bajada' not in x.lower())
        for p in paragraphs[:3]:
            text = p.get_text(' ', strip=True)
            if len(text.split()) > 5:  # Filtrar textos cortos
                content.append(f"• {text}")
        
        if not content:
            full_text = ' '.join(news_item.get_text(' ', strip=True).split()[:150])
            content = [f"• {full_text}..."]
        
        # Formatear salida
        return (
            f"📌 {title_text}\n\n" +
            "\n".join(content) +
            "\n\n🔗 Fuente: Al Calor Político"
        )
        
    except Exception as e:
        return f"⛔ Error técnico: {str(e)}"

if __name__ == "__main__":
    noticia = scrape_single_news()
    with open("noticia.txt", "w", encoding="utf-8") as f:
        f.write(noticia)
