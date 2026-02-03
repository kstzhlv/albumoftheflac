# Standard
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
import chardet

# Third party
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

def get_year_from_album_page(html_content: str) -> str:
    soup = BeautifulSoup(html_content, "html.parser")    

    meta_description = soup.find("meta", attrs={"name": "Description"})
    if meta_description and "content" in meta_description.attrs:
        content = meta_description["content"].lower()
        if "released in " in content:
            year = content.split("released in ")[1][0:4]
        else:
            raise Exception(f"Failed to parse year from AOTY")

    return year
