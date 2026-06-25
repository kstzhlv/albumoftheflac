# Standard
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

# Third party
import chardet
from bs4 import BeautifulSoup
from loguru import logger

BASE_LINK = "https://www.albumoftheyear.org/"
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (X11; Linux x86_64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/134.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
}


def create_link_for_search(artist_tag: str, album_tag: str):
    return f"{BASE_LINK}search/?q={artist_tag}+{album_tag}"


def create_link_for_album_page(album_link: str):
    return f"{BASE_LINK}{album_link}"


def log_response_headers(response) -> None:
    status = getattr(response, "status", None) or getattr(response, "code", None)
    reason = getattr(response, "reason", None)

    if reason:
        logger.debug("Response status: {} {}", status, reason)
    else:
        logger.debug("Response status: {}", status)

    for name, value in response.headers.items():
        logger.debug("Response header: {}: {}", name, value)


def fetch_page(url: str) -> str:
    request = Request(url, headers=HEADERS)

    try:
        logger.debug("Fetching page: {}", url)

        with urlopen(request) as response:
            log_response_headers(response)

            page = response.read()
            encoding = chardet.detect(page)["encoding"] or "utf-8"

            logger.debug("Detected encoding: {}", encoding)

            return page.decode(encoding, errors="replace")

    except HTTPError as e:
        logger.error("HTTP request failed: {} {}", e.code, e.reason)

        log_response_headers(e)

        raise Exception(f"HTTP request failed: {e.code} {e.reason}") from e

    except URLError as e:
        logger.error("Network request failed: {}", e.reason)

        raise Exception(f"Network error: {e.reason}") from e


def get_album_link(html_content: str) -> str | None:
    soup = BeautifulSoup(html_content, "html.parser")
    a = soup.select_one('.albumBlock a[href*="album/"]')
    href = a["href"] if a else None

    return href


def get_genres_from_album_page(html_content: str) -> str:
    soup = BeautifulSoup(html_content, "html.parser")
    genres = []

    for row in soup.find_all("div", class_="detailRow"):
        label = row.find("span")
        if not label or "Genre" not in label.get_text():
            continue

        genre_links = row.select('a[href*="/genre/"]')
        genres = [
            link.get_text(strip=True)
            for link in genre_links
            if not link.select_one(".secondary")
        ]
        logger.debug("Found primary genres from album details: {}", genres)
        break

    if not genres:
        logger.warning("Genres were not found on album page")

    genres_string = ", ".join(genres)

    return genres_string


def get_date_from_album_page(html_content: str) -> str:
    album_page = BeautifulSoup(html_content, "html.parser")
    release_date_div = album_page.find("div", class_="detailRow")

    return release_date_div.get_text(strip=True)
