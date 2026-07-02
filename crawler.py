import time
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

KEYWORDS = [
    "admissions", "apply", "program", "programs",
    "tuition", "fees", "academics", "degree",
    "major", "minor", "course", "catalog",
    "financial aid", "scholarship"
]

MAX_DEPTH = 2
visited = set()

options = Options()
options.add_argument("--headless=new")
driver = webdriver.Chrome(options=options)


def get_page(url):
    try:
        driver.get(url)
        time.sleep(2)
        return driver.page_source
    except:
        return None


def clean_text(soup):
    return soup.get_text(" ", strip=True)


def crawl(url, domain, depth=0, pages=None):

    if pages is None:
        pages = []

    if depth > MAX_DEPTH or url in visited:
        return pages

    visited.add(url)

    print(f"[Depth {depth}] {url}")

    html = get_page(url)
    if not html:
        return pages

    soup = BeautifulSoup(html, "html.parser")

    pages.append({
        "url": url,
        "text": clean_text(soup)[:12000]
    })

    for a in soup.find_all("a", href=True):

        href = urljoin(url, a["href"])

        if urlparse(href).netloc != domain:
            continue

        text = a.get_text(" ", strip=True).lower()
        href_lower = href.lower()

        if any(k in text or k in href_lower for k in KEYWORDS):
            crawl(href, domain, depth + 1, pages)

    return pages


def close_driver():
    driver.quit()