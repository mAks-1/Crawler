import asyncio
import time
import csv
from collections import deque
from crawl import crawl
from config import start_url

urls = deque([start_url])
visited_urls = set()
products = []

async def main():
    start_time = time.time()
    await crawl(urls, visited_urls, products)
    end_time = time.time()

    print("\nCrawling finished.")
    print(f"Visited {len(visited_urls)} pages.")
    print(f"Execution time: {end_time - start_time:.2f} seconds.")

    # Запис продуктів у CSV
    with open("products.csv", "w", newline="", encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["URL", "Image", "Name", "Price"])

        for product in products:
            writer.writerow(product.values())

    print(f"Saved {len(products)} products to products.csv.")

if __name__ == "__main__":
    asyncio.run(main())
