import requests
from bs4 import BeautifulSoup
import sqlite3
from transformers import pipeline

# Configuración
SITE_URL = "https://www.alcalorpolitico.com/edicion/inicio.html"
DB_NAME = "news.db"

def scrape_alcalor():
    try:
        # Configuración robusta
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept-Language': 'es-MX,es;q=0.9'
        }

        # Intento con timeout
        response = requests.get(SITE_URL, headers=headers, timeout=20)
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

def rewrite_news(text):
    try:
        model = pipeline("text2text-generation", model="facebook/bart-large-cnn")
        rewritten = model(
            f"Reescribe esto de manera única y natural, como un periodista profesional: {text}",
            max_length=1024,
            num_return_sequences=1
        )
        return rewritten[0]['generated_text']
    except Exception as e:
        print(f"Error al reescribir: {e}")
        return text

def save_to_db(content):
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS news (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                content TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        cursor.execute('INSERT INTO news (content) VALUES (?)', (content,))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Error en DB: {e}")

if __name__ == "__main__":
    # 1. Scrapear contenido
    contenido = scrape_alcalor()
    
    # 2. Guardar en archivo temporal
    with open("noticias.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(contenido))
    
    # 3. Procesar y guardar en DB (opcional)
    if not contenido[0].startswith("Error"):
        for texto in contenido:
            texto_reescrito = rewrite_news(texto)
            save_to_db(texto_reescrito)
    
    print("Proceso completado. Ver noticias.txt")
