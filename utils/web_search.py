import requests
import os
from dotenv import load_dotenv

load_dotenv()

SERPER_API_KEY = os.getenv("SERPER_API_KEY")


def search_company(company_name):
    """
    Searches Google using Serper API
    and returns top search snippets.
    """

    url = "https://google.serper.dev/search"

    payload = {
        "q": company_name
    }

    headers = {
        "X-API-KEY": SERPER_API_KEY,
        "Content-Type": "application/json"
    }

    response = requests.post(
        url,
        json=payload,
        headers=headers
    )

    data = response.json()

    results = []

    organic_results = data.get("organic", [])

    for item in organic_results[:5]:
        results.append({
            "title": item.get("title", ""),
            "snippet": item.get("snippet", ""),
            "link": item.get("link", "")
        })

    return results