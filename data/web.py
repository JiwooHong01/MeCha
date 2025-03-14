from langchain.tools import DuckDuckGoSearchRun
import requests
from bs4 import BeautifulSoup


def search_web(query):
    search = DuckDuckGoSearchRun()
    results = search.run(query)
    return results  # URL과 요약 포함된 결과 반환

def scrape_website(url):
    try:
        response = requests.get(url, timeout=5)
        soup = BeautifulSoup(response.text, "html.parser")
        return soup.get_text()[:10000]  # 처음 1000자만 반환하여 요약
    except Exception as e:
        return f"Failed to fetch content: {str(e)}"

