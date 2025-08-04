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
        
        # Extracción directa de todos los textos importantes
        textos = []
        for element in soup.find_all(['h1', 'h2', 'h3', 'p']):
            text = element.get_text(strip=True)
            if len(text) > 20:  # Filtrar textos cortos
                textos.append(text)
        
        return textos[:10] if textos else ["Prueba exitosa pero sin contenido - necesita ajustes manuales"]

    except Exception as e:
        return [f"Error de conexión: {str(e)}"]

if __name__ == "__main__":
    contenido = scrape_alcalor()
    with open("noticias.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(contenido))
