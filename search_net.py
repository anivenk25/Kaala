# search_net.py
try:
    from duckduckgo_search import DDGS
    _DDGS_AVAILABLE = True
except ImportError:
    _DDGS_AVAILABLE = False
    print("[Warning] 'duckduckgo_search' library not found; falling back to manual HTML scraping for text searches.")
import json
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs, unquote

def manual_text_search(query, num_results):
    """Fallback text search using DuckDuckGo HTML scraping."""
    search_url = "https://html.duckduckgo.com/html/"
    params = {"q": query}
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        resp = requests.get(search_url, params=params, timeout=10, headers=headers)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")
        anchors = soup.find_all("a", class_="result__a", href=True)
        results = []
        for a in anchors:
            href = a["href"]
            if "uddg=" in href:
                parsed = urlparse(href, scheme="https")
                qs = parse_qs(parsed.query)
                uddg = qs.get("uddg")
                if uddg:
                    real_url = unquote(uddg[0])
                else:
                    continue
            else:
                real_url = href
                if real_url.startswith("//"):
                    real_url = "https:" + real_url
            results.append(real_url)
            if len(results) >= num_results:
                break
        return results
    except Exception as e:
        print(f"[Manual DDG Search Error] {e}")
        return []


class DuckDuckGoSearchManager:
    """
    A class to perform various types of web searches using DuckDuckGo.
    """

    def __init__(self):
        self.default_results = 3
        self.headers = {"User-Agent": "Mozilla/5.0"}
        self.use_ddgs = _DDGS_AVAILABLE

    def _get_results(self, search_func, *args, num_results=None):
        try:
            with DDGS() as ddgs:
                results = search_func(ddgs, *args, max_results=num_results or self.default_results)
                return results
        except Exception as e:
            print(f"[DDG Search Error] {e}")
            return []

    def text_search(self, query, num_results=None):
        # Determine number of results to fetch
        max_results = num_results or self.default_results
        # Attempt DuckDuckGoSearch library if available
        if getattr(self, "use_ddgs", False):
            results = self._get_results(
                lambda ddgs, **kwargs: ddgs.text(query, **kwargs),
                num_results=max_results
            )
            if results:
                return [res.get("href") for res in results if "href" in res]
        # Fallback to manual HTML scraping
        return manual_text_search(query, max_results)

    def news_search(self, query, num_results=None):
        results = self._get_results(lambda ddgs, **kwargs: ddgs.news(query, **kwargs), num_results=num_results)
        return [result.get('url') for result in results if 'url' in result]

    def images_search(self, query, num_results=None):
        results = self._get_results(lambda ddgs, **kwargs: ddgs.images(query, **kwargs), num_results=num_results)
        return [
            {
                'image': result.get('image'),
                'thumbnail': result.get('thumbnail')
            } for result in results if 'image' in result and 'thumbnail' in result
        ]

    def videos_search(self, query, num_results=None):
        results = self._get_results(lambda ddgs, **kwargs: ddgs.videos(query, **kwargs), num_results=num_results)
        return [
            {
                'title': result.get('title', 'No title'),
                'content': result.get('content', '')
            } for result in results
        ]

    def maps_search(self, query, place, num_results=None):
        results = self._get_results(lambda ddgs, **kwargs: ddgs.maps(query, place, **kwargs), num_results=num_results)
        return [
            {
                'title': result.get('title', 'No title'),
                'address': result.get('address', 'No address'),
                'phone': result.get('phone', 'Not available'),
                'url': result.get('url', 'Not available'),
                'operating_hours': result.get('hours', 'Not available')
            } for result in results
        ]

    def get_answer_box(self, query):
        try:
            with DDGS() as ddgs:
                results = list(ddgs.answers(query))
                return results[0] if results else {"answer": "No direct answer found"}
        except Exception as e:
            print(f"[Answer Box Error] {e}")
            return {"answer": "Error fetching answer"}

    def get_train_status(self, train_number, station=None):
        query = f"{train_number} train running status"
        links = self.text_search(query, num_results=5)
        priority_sites = ["runningstatus.in", "trainspnrstatus.com", "trainman.in"]

        for url in links:
            if any(site in url for site in priority_sites):
                try:
                    resp = requests.get(url, timeout=5, headers=self.headers)
                    soup = BeautifulSoup(resp.text, 'html.parser')
                    text = soup.get_text(separator="\n")

                    if station:
                        for line in text.splitlines():
                            if station.lower() in line.lower():
                                return {"station": station, "info": line.strip()}
                    else:
                        preview = "\n".join([line.strip() for line in text.splitlines() if line.strip()][:5])
                        return {"station": "N/A", "info": preview}
                except Exception as e:
                    print(f"[Train Status Error] {e}")
        return {"error": "Unable to fetch train status"}

    def define_word(self, word):
        query = f"define {word}"
        results = self.text_search(query, num_results=3)
        for url in results:
            try:
                response = requests.get(url, timeout=5, headers=self.headers)
                soup = BeautifulSoup(response.text, 'html.parser')
                paragraphs = soup.find_all('p')
                for para in paragraphs:
                    text = para.get_text(strip=True)
                    if word.lower() in text.lower():
                        return {"word": word, "definition": text}
            except Exception:
                continue
        return {"word": word, "definition": "Definition not found."}

    def get_event_info(self, query):
        return search_internet(query + " event time and location", num_results=3)


def search_internet(query: str, num_results: int = 5) -> list:
    print(f"[search_internet] Searching DuckDuckGo for: {query}")
    ddg = DuckDuckGoSearchManager()
    urls = ddg.text_search(query, num_results=num_results)

    final_results = []
    headers = {"User-Agent": "Mozilla/5.0"}

    for url in urls:
        try:
            response = requests.get(url, timeout=5, headers=headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')

            title = soup.title.string.strip() if soup.title and soup.title.string else url
            desc_tag = soup.find("meta", attrs={"name": "description"}) or soup.find("p")
            snippet = desc_tag.get("content", "").strip() if desc_tag else ""

            if not snippet and desc_tag:
                snippet = desc_tag.get_text(strip=True)

            final_results.append({
                "title": title,
                "url": url,
                "snippet": snippet
            })

        except Exception as e:
            print(f"[search_internet] Error scraping {url}: {e}")
            final_results.append({
                "title": url,
                "url": url,
                "snippet": ""
            })

    return final_results




