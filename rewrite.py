import openai
import json

def improve_news(news_data, api_key):
    try:
        openai.api_key = api_key
        
        prompt = f"""
        Reescribe esta noticia de forma completamente original, manteniendo los hechos pero con:
        - Estructura profesional
        - Tono periodístico neutro
        - Redacción 100% única (evita plagio)
        - Incluye contexto relevante si es necesario

        Datos originales:
        Título: {news_data['title']}
        Contenido: {news_data['content']}

        Devuelve SOLO un JSON con:
        {{
            "new_title": "Título mejorado",
            "new_content": "Texto reescrito"
        }}
        """
        
        response = openai.ChatCompletion.create(
            model="gpt-4-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7  # Balance entre creatividad y precisión
        )
        
        return json.loads(response.choices[0].message.content)
    
    except Exception as e:
        print(f"⛔ Error en IA: {e}")
        return None
