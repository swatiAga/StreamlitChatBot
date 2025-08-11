# import pandas as pd
# from urllib.parse import urljoin, urlparse
# import requests
# from bs4 import BeautifulSoup


# def crawl_website(start_url):
#     visited = set()
#     queue = [start_url]
#     result_data = []
#     base_domain = urlparse(start_url).netloc

#     headers = {
#         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
#     }

#     while queue:
#         current_url = queue.pop(0)
#         if current_url in visited:
#             continue

#         if any(x in current_url for x in ["linkedin", "youtube", "instagram"]) or current_url.endswith(".pdf"):
#             continue

#         if urlparse(current_url).netloc != base_domain:
#             continue

#         visited.add(current_url)

#         try:
#             response = requests.get(current_url, headers=headers)
#             response.raise_for_status()
#             soup = BeautifulSoup(response.content, "html.parser")

#             title = soup.find("title").get_text() if soup.find("title") else "No title"
#             meta_desc = soup.find("meta", {"name": "description"}) or soup.find("meta", {"property": "og:description"})
#             meta_desc = meta_desc["content"] if meta_desc else "No description"

#             headings = {f"h{i}": [tag.get_text(strip=True) for tag in soup.find_all(f"h{i}")] for i in range(1, 7)}
#             paragraphs = [p.get_text(strip=True) for p in soup.find_all("p")]
#             links = [urljoin(current_url, a["href"]) for a in soup.find_all("a", href=True) if urlparse(urljoin(current_url, a["href"])).netloc == base_domain]

#             result_data.append({
#                 "URL": current_url,
#                 "Title": title,
#                 "Meta Description": meta_desc,
#                 "Headings": headings,
#                 "Paragraphs": paragraphs,
#                 "Links": links
#             })
#             sum=0
#             for link in soup.find_all("a", href=True):
#                 sum=sum+1
#                 full_url = urljoin(current_url, link["href"])
#                 if urlparse(full_url).netloc == base_domain and full_url not in visited and sum < 100:
#                     queue.append(full_url)
                  
                

#         except requests.RequestException:
#             continue

#     df = pd.DataFrame(result_data)
#     df.to_excel("website_scrape.xlsx", index=False)
#     return df

import pandas as pd
from urllib.parse import urljoin, urlparse
import requests
from bs4 import BeautifulSoup


def crawl_website(start_url, max_links=50):
    visited = set()
    queue = [start_url]
    base_domain = urlparse(start_url).netloc
    processed_links = 0  # Counter to track the number of links processed

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    while queue and processed_links < max_links:
        current_url = queue.pop(0)
        if current_url in visited:
            continue

        # Skip unwanted URLs
        if any(x in current_url for x in ["linkedin", "youtube", "instagram"]) or current_url.endswith(".pdf"):
            continue

        # Ensure the URL belongs to the same domain
        if urlparse(current_url).netloc != base_domain:
            continue

        visited.add(current_url)

        try:
            response = requests.get(current_url, headers=headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, "html.parser")

            # Extract data
            title = soup.find("title").get_text() if soup.find("title") else "No title"
            meta_desc = soup.find("meta", {"name": "description"}) or soup.find("meta", {"property": "og:description"})
            meta_desc = meta_desc["content"] if meta_desc else "No description"
            headings = {f"h{i}": [tag.get_text(strip=True) for tag in soup.find_all(f"h{i}")] for i in range(1, 7)}
            paragraphs = [p.get_text(strip=True) for p in soup.find_all("p")]
            links = [urljoin(current_url, a["href"]) for a in soup.find_all("a", href=True) if urlparse(urljoin(current_url, a["href"])).netloc == base_domain]

            # Yield the current URL's data as a dictionary
            yield {
                "URL": current_url,
                "Title": title,
                "Meta Description": meta_desc,
                "Headings": headings,
                "Paragraphs": paragraphs,
                "Links": links
            }

            # Add new links to the queue
            for link in soup.find_all("a", href=True):
                sum=0
                sum=sum+1
                full_url = urljoin(current_url, link["href"])
                if urlparse(full_url).netloc == base_domain and full_url not in visited and sum < 25:
                    queue.append(full_url)

            processed_links += 1  # Increment the processed links counter

        except requests.RequestException:
            continue