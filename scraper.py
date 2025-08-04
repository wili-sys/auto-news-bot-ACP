import requests
from bs4 import BeautifulSoup

def scrape_single_news():
    try:
        url = "https://www.alcalorpolitico.com/edicion/inicio.html"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept-Language': 'es-MX,es;q=0.9'
        }
        
        response = requests.get(url, headers=headers, timeout=20)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Estrategia 1: Buscar la noticia principal
        main_news = soup.find('article') or soup.find(class_=lambda x: x and ('noticia-principal' in x or 'destacada' in x))
        
        if not main_news:
            # Estrategia 2: Buscar cualquier noticia
            news_candidates = soup.find_all(['article', 'div'], class_=lambda x: x and ('noticia' in x or 'articulo' in x))
            main_news = news_candidates[0] if news_candidates else None
        
        if main_news:
            # Extraer título
            title = main_news.find(['h1', 'h2', 'h3'])
            title_text = title.get_text(strip=True) if title else "Noticia sin título"
            
            # Extraer contenido (los primeros 5 párrafos relevantes)
            content = []
            paragraphs = main_news.find_all('p')
            for p in paragraphs[:5]:  # Limitar a 5 párrafos
                text = p.get_text(strip=True)
                if len(text.split()) > 5:  # Filtrar textos muy cortos
                    content.append(f"• {text}")
            
            if not content:
                full_text = ' '.join(main_news.get_text(' ', strip=True).split()[:150]) + "..."
                content = [f"• {full_text}"]
            
            # Formatear la noticia única
            news_output = (
                f"📌 {title_text}\n\n" +
                "\n".join(content) +
                "\n\n🔗 Fuente: Al Calor Político"
            )
            return news_output
        else:
            return "⚠️ No se pudo encontrar ninguna noticia en la página principal"
    
    except Exception as e:
        return f"⛔ Error al obtener la noticia: {str(e)}"

if __name__ == "__main__":
    noticia = scrape_single_news()
    with open("noticia.txt", "w", encoding="utf-8") as f:
        f.write(noticia)
