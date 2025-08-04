import requests
from bs4 import BeautifulSoup

def scrape_alcalor():
    try:
        url = "https://www.alcalorpolitico.com/edicion/inicio.html"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept-Language': 'es-MX,es;q=0.9'
        }
        
        response = requests.get(url, headers=headers, timeout=20)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        resultados = []
        noticias = soup.find_all('article')  # Busca elementos <article> (donde suelen estar las noticias)
        
        for noticia in noticias[:10]:  # Limita a 10 noticias para prueba
            titulo = noticia.find(['h2', 'h3'])
            if not titulo:
                continue
                
            contenido = []
            # Extrae párrafos de la noticia (ajusta según la estructura real)
            for p in noticia.find_all('p', class_=lambda x: x and 'bajada' not in x):
                texto = p.get_text(strip=True)
                if len(texto) > 20:  # Filtra textos cortos
                    contenido.append(f"• {texto}")
            
            if not contenido:
                contenido = ["• Contenido no disponible (ver enlace original)"]
            
            # Formato de salida
            resultados.append(
                f"📌 {titulo.get_text(strip=True)}\n" +
                "\n".join(contenido) +
                "\n══════════════════════════════════════════════════\n"
            )
        
        return resultados if resultados else ["⚠️ No se encontraron noticias con el formato esperado"]

    except Exception as e:
        return [f"⛔ Error técnico: {str(e)}"]

if __name__ == "__main__":
    noticias = scrape_alcalor()
    with open("noticias.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(noticias))
