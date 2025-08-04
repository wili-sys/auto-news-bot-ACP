import requests
from bs4 import BeautifulSoup

def scrape_alcalor_completo():
    url = "https://www.alcalorpolitico.com/edicion/inicio.html"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Referer': 'https://www.alcalorpolitico.com'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=20)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        resultados = []
        
        # 1. Extraer noticias principales (selectores actualizados agosto 2024)
        articulos = soup.select('div.noticia-principal, div.noticia-secundaria, article.card')
        
        for articulo in articulos[:5]:  # Limitar a 5 noticias para prueba
            # Extraer título
            titulo = articulo.select_one('h2.titulo, h3.titulo, h2.card-title, h3.card-title')
            
            if titulo:
                noticia = {
                    'titulo': titulo.text.strip(),
                    'contenido': []
                }
                
                # Extraer contenido (párrafos)
                contenido = articulo.select('p:not([class]), p.contenido, p.card-text')
                for p in contenido[:3]:  # Primeros 3 párrafos
                    if p.text.strip():
                        noticia['contenido'].append(p.text.strip())
                
                if noticia['contenido']:
                    # Plan B: Extraer texto cercano
                    texto = articulo.get_text(separator=' ', strip=True)
                    noticia['contenido'] = [' '.join(texto.split()[:50]) + '...']  # Limitar a 50 palabras
                
                # Formatear resultado
                resultado = f"TÍTULO: {noticia['titulo']}\n"
                resultado += "CONTENIDO:\n" + "\n".join(f"- {p}" for p in noticia['contenido'])
                resultado += "\n────────────────────"
                resultados.append(resultado)
        
        return resultados if resultados else ["Error: Revisar selectores - estructura del sitio cambiada"]

    except Exception as e:
        return [f"Error de conexión: {str(e)}"]

if __name__ == "__main__":
    noticias = scrape_alcalor_completo()
    with open("noticias.txt", "w", encoding="utf-8") as f:
        f.write("\n\n".join(noticias))
