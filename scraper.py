import requests
from bs4 import BeautifulSoup
from datetime import datetime

def scrape_alcalor():
    url = "https://www.alcalorpolitico.com/edicion/inicio.html"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept-Language': 'es-MX,es;q=0.9'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=20)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extraer TODAS las noticias
        news_items = []
        
        # 1. Noticias principales (destacadas)
        for article in soup.select('article.noticia-principal, article.noticia-secundaria'):
            title = article.find('h2', class_='titulo-noticia')
            if title:
                news_items.append(f"PRINCIPAL: {title.text.strip()}")
        
        # 2. Nota Roja
        nota_roja = soup.find('section', id='nota-roja')
        if nota_roja:
            for item in nota_roja.select('h3.titulo'):
                news_items.append(f"NOTA ROJA: {item.text.strip()}")
        
        # 3. Otras secciones
        sections = {
            'POLÍTICA': 'section-politica',
            'NACIONAL': 'section-nacional',
            'INTERNACIONAL': 'section-internacional'
        }
        
        for section_name, section_id in sections.items():
            section = soup.find('section', id=section_id)
            if section:
                for item in section.select('h3.titulo-noticia'):
                    news_items.append(f"{section_name}: {item.text.strip()}")
        
        # Formatear resultado
        if not news_items:
            return ["Error: No se capturaron noticias - Revisar selectores"]
            
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        return [f"Última actualización: {timestamp}\n"] + news_items

    except Exception as e:
        return [f"Error técnico: {str(e)}"]

if __name__ == "__main__":
    news = scrape_alcalor()
    with open("noticias.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(news))
