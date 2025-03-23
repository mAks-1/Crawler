from urllib.parse import urljoin
import aiohttp
from bs4 import BeautifulSoup
from config import MAX_PAGES, start_url
from fetching import fetch

async def crawl(urls, visited_urls, products):
    """Асинхронний обхід сторінок."""
    async with aiohttp.ClientSession() as session:
        while urls and len(visited_urls) < MAX_PAGES:
            current_url = urls.popleft()

            if current_url in visited_urls:
                continue

            html = await fetch(session, current_url)

            if html:
                visited_urls.add(current_url)
                soup = BeautifulSoup(html, "html.parser")

                link_elements = soup.select("a[href]")
                print(f"Found {len(link_elements)} links on {current_url}")

                for link_element in link_elements:
                    raw_url = link_element["href"]
                    full_url = urljoin(current_url, raw_url)

                    if (
                        start_url in full_url
                        and full_url not in visited_urls
                        and full_url not in urls
                    ):
                        urls.append(full_url)

                product = {
                    "url": current_url,
                    "image": None,
                    "name": None,
                    "price": None
                }

                image_element = soup.select_one(".wp-post-image")
                product["image"] = image_element["src"] if image_element else None

                name_element = soup.select_one(".product_title")
                product["name"] = name_element.text.strip() if name_element else None

                price_element = soup.select_one(".price")
                product["price"] = price_element.text.strip() if price_element else None

                if product["name"]:
                    products.append(product)
