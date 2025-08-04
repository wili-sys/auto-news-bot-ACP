import requests
from bs4 import BeautifulSoup
import time

def scrape_alcalor():
    try:
        # Configuración robusta
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept-Language': 'es-MX,es;q=0.9'
        }
        
        # Intento con timeout
        response = requests.get("https://www.alcalorpolitico.com/edicion/inicio.html", 
                             headers=headers, timeout=20)
        response.raise_for_status()
        
        # Parseo seguro
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extracción mejorada con separadores
        resultados = []
        current_news = []
        
        for element in soup.find_all(['h1', 'h2', 'h3', 'p']):
            text = element.get_text(strip=True)
            
            if len(text) > 20:  # Filtrar textos cortos
                # Si es un título (h1-h3), comenzar nueva noticia
                if element.name in ['h1', 'h2', 'h3'] and current_news:
                    # Guardar noticia anterior antes de comenzar nueva
                    resultados.append("\n".join(current_news))
                    resultados.append("\n" + "═"*50 + "\n")  # Separador visual
                    current_news = []
                
                # Añadir elemento a la noticia actual
                if element.name in ['h1', 'h2', 'h3']:
                    current_news.append(f"📌 {text.upper()}")
                else:
                    current_news.append(f"• {text}")
        
        # Añadir la última noticia
        if current_news:
            resultados.append("\n".join(current_news))
        
        return resultados if resultados else ["⚠️ No se encontraron noticias con el formato esperado"]

    except Exception as e:
        return [f"⛔ Error de conexión: {str(e)}"]

if __name__ == "__main__":
    contenido = scrape_alcalor()
    with open("noticias.txt", "w", encoding="utf-8") as f:
        f.write("\n\n".join(contenido))
