def improve_news(text):
    if "⚠️" in text or "⛔" in text:
        return text  # No procesar mensajes de error
    
    # Simulador de mejoras (en producción usaría IA real)
    improvements = [
        "🔍 Análisis completo:",
        "📰 Reportaje ampliado:",
        "✨ Perspectiva mejorada:"
    ]
    
    return (
        f"{random.choice(improvements)}\n\n" +
        text.replace("•", "➡") +  # Cambiar viñetas
        "\n\n💡 Nota optimizada con tecnología"
    )

if __name__ == "__main__":
    import random
    
    try:
        with open("noticia_completa.txt", "r", encoding="utf-8") as f:
            original = f.read()
        
        mejorada = improve_news(original)
        
        with open("noticia_mejorada.txt", "w", encoding="utf-8") as f:
            f.write(mejorada)
            
    except Exception as e:
        with open("noticia_mejorada.txt", "w", encoding="utf-8") as f:
            f.write(f"Error al mejorar la noticia: {str(e)}")
