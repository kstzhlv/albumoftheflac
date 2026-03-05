# Standard
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

# Third party
import chardet
from bs4 import BeautifulSoup

BASE_LINK = "https://www.albumoftheyear.org/"
HEADERS = {"User-Agent": "Mozilla/6.0"}


def create_link_for_search(artist_tag: str, album_tag: str):
    return f"{BASE_LINK}search/?q={artist_tag}+{album_tag}"


def create_link_for_album_page(album_link: str):
    return f"{BASE_LINK}{album_link}"


def fetch_page(url: str) -> str:
    try:
        request = Request(url, headers=HEADERS)
        page = urlopen(request).read()
        encoding = chardet.detect(page)["encoding"]
    except (URLError, HTTPError) as e:
        raise Exception(f"Failed to fetch page: {e}")

    return page.decode(encoding, errors="replace")


def get_album_link(html_content: str) -> str | None:
    soup = BeautifulSoup(html_content, "html.parser")
    a = soup.select_one('.albumBlock a[href*="album/"]')
    href = a["href"] if a else None

    return href


def get_genres_from_album_page(html_content: str) -> str:
    soup = BeautifulSoup(html_content, "html.parser")
    genre_meta_tags = soup.find_all("meta", itemprop="genre")
    genres = [tag.get("content") for tag in genre_meta_tags]
    genres_string = ", ".join(genres)

    return genres_string


def get_date_from_album_page(html_content: str) -> str:
    album_page = BeautifulSoup(html_content, "html.parser")
    release_date_div = album_page.find("div", class_="detailRow")

    return release_date_div.get_text(strip=True)
