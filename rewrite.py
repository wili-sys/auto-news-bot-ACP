def rewrite_with_ai(text):
    # Aquí deberías usar una API de IA (DeepSeek, Hugging Face, etc.)
    # Por ahora simulamos la reescritura:
    return f"📢 OPTIMIZADO: {text} (simulación de IA)"

if __name__ == "__main__":
    with open("noticias.txt", "r", encoding="utf-8") as file:
        news = file.readlines()
    
    rewritten_news = [rewrite_with_ai(n.strip()) for n in news if n.strip()]
    
    with open("noticias_reescritas.txt", "w", encoding="utf-8") as file:
        file.write("\n".join(rewritten_news))
