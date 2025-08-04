from scraper import scrape_full_news
from rewriter import improve_news
from config import OPENAI_API_KEY, TARGET_URL
import time

def main():
    # Paso 1: Extraer noticia
    print("🔍 Extrayendo noticia de Al Calor Político...")
    news_data = scrape_full_news(TARGET_URL)  # Usa la URL de config.py
    
    if not news_data:
        print("⛔ Error: No se pudo extraer la noticia. Revisa:")
        print("- ¿La URL en config.py es correcta y directa a una noticia?")
        print("- ¿Los selectores en scraper.py coinciden con el HTML del sitio?")
        return
    
    print("\n📰 **Noticia original:**")
    print(f"Título: {news_data['title']}")
    print(f"Contenido (extracto): {news_data['content'][:150]}...\n")  # Muestra un preview

    # Paso 2: Mejorar con IA
    print("🔄 Reescribiendo noticia con IA...")
    improved_news = improve_news(news_data, OPENAI_API_KEY)
    
    if not improved_news:
        print("⛔ Error al reescribir. Verifica:")
        print("- ¿Tu API key de OpenAI en config.py es válida?")
        print("- ¿Hay créditos suficientes en tu cuenta de OpenAI?")
        return
    
    # Paso 3: Guardar resultado
    timestamp = time.strftime("%Y%m%d_%H%M")  # Ej: 20240615_1423
    output_filename = f"noticia_mejorada_{timestamp}.txt"
    
    with open(output_filename, "w", encoding="utf-8") as f:
        f.write(f"✨ {improved_news['new_title']}\n\n")
        f.write(improved_news['new_content'])
        f.write(f"\n\n🔗 Fuente original: {news_data['url']}")
    
    print(f"\n✅ **Noticia mejorada guardada como:** {output_filename}")
    print("¡Proceso completado! 🎉")

if __name__ == "__main__":
    main()
