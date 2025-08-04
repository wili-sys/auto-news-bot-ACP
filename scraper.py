import requests
from bs4 import BeautifulSoup
import random
import time

def get_random_headers():
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0'
    ]
    return {
        'User-Agent': random.choice(user_agents),
        'Accept-Language': 'es-MX,es;q=0.9',
        'Referer': 'https://www.google.com/',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'DNT': '1'
    }

def scrape_alcalor_politico():
    url = "https://www.alcalorpolitico.com/edicion/inicio.html"
    
    try:
        # Intentar con diferentes configuraciones
        for attempt in range(3):
            try:
                # Espera aleatoria entre intentos
                if attempt > 0:
                    time.sleep(random.uniform(2, 5))
                
                response = requests.get(
                    url,
                    headers=get_random_headers(),
                    timeout=15,
                    cookies={'cookie_consent': 'true'}
                )
                response.raise_for_status()
                
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Extracción mejorada con múltiples estrategias
                news_items = []
                
                # Estrategia 1: Buscar artículos con estructura común
                articles = soup.find_all('article', limit=5) or soup.find_all('div', class_=lambda x: x and 'noticia' in x.lower(), limit=5)
                
                for article in articles:
                    # Extraer título
                    title = article.find(['h2', 'h3', 'h4']) or article.find(attrs={'itemprop': 'headline'})
                    if not title:
                        continue
                    
                    # Extraer contenido
                    content = []
                    # Buscar párrafos principales
                    paragraphs = article.find_all('p', limit=3) or [article]
                    for p in paragraphs:
                        text = p.get_text(' ', strip=True)
                        if len(text.split()) > 5:  # Filtrar textos muy cortos
                            content.append(text)
                    
                    # Si no hay contenido, usar texto completo
                    if not content:
                        full_text = article.get_text(' ', strip=True)
                        content = [' '.join(full_text.split()[:50]) + '...']
                    
                    # Formatear resultado
                    news_item = (
                        f"📌 TÍTULO: {title.get_text(strip=True)}\n"
                        f"📝 CONTENIDO:\n" + 
                        "\n".join(f"• {p}" for p in content) +
                        "\n―――――――――――――――――――――――――――――――――――――――"
                    )
                    news_items.append(news_item)
                
                if news_items:
                    return news_items
                
            except Exception as e:
                if attempt == 2:  # Último intento
                    raise e
                continue
        
        # Si todo falla, usar API de respaldo
        return get_news_backup()
        
    except Exception as e:
        return [f"⚠️ No se pudieron obtener noticias. Razón: {str(e)}"]

def get_news_backup():
    """Alternativa usando NewsAPI si el scraping falla"""
    try:
        # Esto es un ejemplo - necesitarías una API key real
        api_key = "TU_API_KEY"  # Obtén una gratis en newsapi.org
        url = f"https://newsapi.org/v2/top-headlines?country=mx&apiKey={api_key}"
        response = requests.get(url).json()
        
        return [
            f"📰 {article['title']}\n"
            f"📝 {article.get('description', 'Descripción no disponible')}\n"
            f"🔗 {article['url']}\n"
            "―――――――――――――――――――――――――――――――――――――――"
            for article in response.get('articles', [])[:3]
        ]
    except:
        return ["📢 No se pudieron cargar noticias. Por favor intente más tarde."]

if __name__ == "__main__":
    news = scrape_alcalor_politico()
    with open("noticias.txt", "w", encoding="utf-8") as f:
        f.write("\n\n".join(news))
