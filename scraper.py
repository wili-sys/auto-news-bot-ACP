import requests
from bs4 import BeautifulSoup

def scrape_news():
    url = "https://www.bbc.com/mundo"  # Cambia al sitio que quieras scrapear
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    headlines = soup.find_all('h3')  # Ajusta según la estructura del sitio
    
    news_list = []
    for headline in headlines[:5]:  # Solo las primeras 5 noticias
        title = headline.text.strip()
        if title and len(title) > 10:
            news_list.append(title)
    
    return news_list

if __name__ == "__main__":
    news = scrape_news()
    with open("noticias.txt", "w", encoding="utf-8") as file:
        file.write("\n".join(news))
