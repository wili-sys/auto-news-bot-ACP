import requests
from bs4 import BeautifulSoup
import re

def scrape_alcalor_actualizado():
    url = "https://www.alcalorpolitico.com/edicion/inicio.html"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
        'Accept-Language': 'es-MX,es;q=0.9',
        'Referer': 'https://www.google.com/'
    }
    
    try:
        # 1. Descargar el HTML
        response = requests.get(url, headers=headers, timeout=25)
        response.raise_for_status()
        
        # 2. Analizar con BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 3. Extracción AGRESIVA (para superar cambios de estructura)
        resultados = []
        
        # Patrón para identificar noticias
        patron_noticias = re.compile(r'noticia|articulo|post|card|contenido', re.I)
        
        # Buscar en TODOS los contenedores posibles
        for contenedor in soup.find_all(['article', 'div', 'section'], class_=patron_noticias):
            # Extraer título de cualquier etiqueta h2-h4
            titulo = contenedor.find(['h2', 'h3', 'h4'])
            if not titulo:
                continue
                
            # Extraer contenido (todos los párrafos)
            contenido = []
            for p in contenedor.find_all('p', recursive=True):
                texto = p.get_text(strip=True)
                if len(texto) > 20:  # Filtrar textos cortos
                    contenido.append(texto)
            
            # Si no hay párrafos, extraer todo el texto
            if not contenido:
                texto_completo = contenedor.get_text(' ', strip=True)
                contenido = [texto_completo[:300] + "..."]  # Limitar longitud
            
            # Formatear resultado
            resultado = (
                f"🚀 TÍTULO: {titulo.get_text(strip=True)}\n"
                f"📌 CONTENIDO:\n" + 
                "\n".join(f"• {p}" for p in contenido[:3]) +  # Mostrar primeros 3 párrafos
                "\n🔗 Fuente: Al Calor Político\n" +
                "―"*50
            )
            resultados.append(resultado)
            
            # Limitar a 5 noticias para prueba
            if len(resultados) >= 5:
                break
        
        return resultados if resultados else ["⚠️ Error: Usa VPN o revisa manualmente el sitio"]

    except Exception as e:
        return [f"⛔ Error técnico: {str(e)}"]

if __name__ == "__main__":
    noticias = scrape_alcalor_actualizado()
    with open("noticias.txt", "w", encoding="utf-8") as f:
        f.write("\n\n".join(noticias))
