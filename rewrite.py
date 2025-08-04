# rewrite.py
import random

def improve_news(text):
    if "⚠️" in text or "⛔" in text:
        return text  # No reescribir mensajes de error
    
    # Simulador de IA (para producción usar una API real)
    improvements = [
        "Análisis:",
        "Contexto ampliado:",
        "Nuevos detalles:",
        "Perspectiva:"
    ]
    
    return (
        f"{random.choice(improvements)}\n\n" +
        text.replace("•", "→") +  # Cambiar viñetas
        "\n\n💡 Nota mejorada con IA"
    )

if __name__ == "__main__":
    try:
        with open("noticia.txt", "r", encoding="utf-8") as f:
            original = f.read()
        
        mejorada = improve_news(original)
        
        with open("noticia_mejorada.txt", "w", encoding="utf-8") as f:
            f.write(mejorada)
            
    except Exception as e:
        with open("noticia_mejorada.txt", "w", encoding="utf-8") as f:
            f.write(f"Error al mejorar la noticia: {str(e)}")
