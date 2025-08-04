def mejorar_noticia(texto):
    # Simulamos mejora con IA (luego puedes conectar API real)
    if ":" in texto:
        seccion, contenido = texto.split(":", 1)
        return f"🚀 {seccion.upper()} OPTIMIZADA:{contenido} (Fuente: Al Calor Político)"
    return f"📌 {texto}"

if __name__ == "__main__":
    with open("noticias.txt", "r", encoding="utf-8") as f:
        original = f.readlines()
    
    mejoradas = [mejorar_noticia(line.strip()) for line in original if line.strip()]
    
    with open("noticias_reescritas.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(mejoradas))
