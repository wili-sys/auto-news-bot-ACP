import requests
from bs4 import BeautifulSoup
import re

def scrape_full_news():
    try:
        url = "https://www.alcalorpolitico.com/edicion/inicio.html"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
            'Accept-Language': 'es-MX,es;q=0.9'
        }
        
        response = requests.get(url, headers=headers, timeout=25)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 1. Buscar contenedor principal
        news_container = soup.find('article') or soup.find('div', class_=re.compile(r'noticia|articulo|post|card|principal', re.I))
        
        if not news_container:
            return "⚠️ No se pudo encontrar el contenedor de noticias"
        
        # 2. Extraer título
        title = news_container.find(['h1', 'h2', 'h3', 'h4']) or "Noticia de Al Calor Político"
        title_text = title.get_text(strip=True)
        
        # 3. Extraer contenido completo
        content = []
        paragraphs = news_container.find_all('p')
        
        for p in paragraphs:
            text = p.get_text(' ', strip=True)
            if len(text.split()) > 3:
                clean_text = ' '.join(text.split())
                content.append(f"• {clean_text}")
        
        if not content:
            full_text = ' '.join(news_container.get_text(' ', strip=True).split())
            content = [f"• {full_text}"]
        
        # 4. Formatear salida
        news_output = (
            f"📌 {title_text}\n\n" +
            "\n".join(content) +
            "\n\n🔗 Fuente: Al Calor Político"
        )
        
        return news_output
        
    except Exception as e:
        return f"⛔ Error: {str(e)}"

if __name__ == "__main__":
    noticia_completa = scrape_full_news()
    with open("noticia_completa.txt", "w", encoding="utf-8") as f:
        f.write(noticia_completa)
