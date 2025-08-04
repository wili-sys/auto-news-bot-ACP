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
        
        # Estrategia 1: Buscar contenedores de noticias por clase común
        contenedores = soup.find_all(class_=lambda x: x and ('noticia' in x or 'articulo' in x or 'post' in x or 'card' in x))
        
        # Estrategia 2: Si falla, buscar por estructura semántica
        if not contenedores:
            contenedores = soup.find_all(['article', 'section', 'div'], limit=20)
        
        for cont in contenedores[:15]:  # Limitar a 15 elementos para prueba
            # Extraer título (h1-h4)
            titulo = cont.find(['h1', 'h2', 'h3', 'h4'])
            if not titulo:
                continue
                
            # Extraer contenido (párrafos)
            contenido = []
            for p in cont.find_all('p'):
                texto = p.get_text(strip=True)
                if len(texto.split()) > 5:  # Filtrar textos muy cortos
                    contenido.append(f"• {texto}")
            
            # Si no hay párrafos, extraer texto completo
            if not contenido:
                texto_completo = ' '.join(cont.get_text(' ', strip=True).split()[:100]) + "..."
                contenido = [f"• {texto_completo}"]
            
            # Formatear resultado
            resultados.append(
                f"📌 {titulo.get_text(strip=True)}\n" +
                "\n".join(contenido[:3]) +  # Mostrar solo primeros 3 párrafos
                "\n══════════════════════════════════════════════════\n"
            )
        
        return resultados if resultados else ["⚠️ Sitio bloqueó el acceso o cambió su estructura"]
    
    except Exception as e:
        return [f"⛔ Error de conexión: {str(e)}"]

if __name__ == "__main__":
    noticias = scrape_alcalor()
    with open("noticias.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(noticias))
