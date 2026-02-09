# Standard
from pathlib import Path

# Local
from albumoftheflac.aoty_parsing import (
    create_link_for_album_page,
    create_link_for_search,
    fetch_page,
    get_album_link,
    get_genres_from_album_page,
    get_year_from_album_page,
)
from albumoftheflac.tags import export_tags, get_tag, set_tag
from albumoftheflac.text import replace_spaces_with_pluses


async def set_correct_tags(directory: Path):
    # get artist and album tags
    tags = export_tags(directory)
    print(f"tags: {tags}")
    artist = get_tag(tags, "artist")
    album = get_tag(tags, "album")
    print(f"artist and album tags: {artist}, {album}")

    # make artist and album tags suitable for links
    artist_tag = replace_spaces_with_pluses(artist)
    album_tag = replace_spaces_with_pluses(album)
    print(f"artist tag, album tag: {artist_tag}, {album_tag}")

    # get album link from search query
    link_for_search = create_link_for_search(artist_tag, album_tag)
    print(f"link for search: {link_for_search}")
    search_content = fetch_page(link_for_search)
    album_link = get_album_link(search_content)
    print(f"album link: {album_link}")

    # get album page from album link
    if album_link is None:
        raise Exception("Album link is invalid")
    link_for_album_page = create_link_for_album_page(album_link)
    album_page = fetch_page(link_for_album_page)

    # get genres and year from album page
    genres = get_genres_from_album_page(album_page)
    year = get_year_from_album_page(album_page)

    # set tags
    set_tag(directory, "date", year)
    set_tag(directory, "genre", genres)
