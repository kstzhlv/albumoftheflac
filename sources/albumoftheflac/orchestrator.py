# Standard
from datetime import datetime
from pathlib import Path

# Third party
from loguru import logger

# Local
from albumoftheflac.aoty_parsing import (
    create_link_for_album_page,
    create_link_for_search,
    fetch_page,
    get_album_link,
    get_date_from_album_page,
    get_genres_from_album_page,
)
from albumoftheflac.tags import export_tags, get_tag, set_tag
from albumoftheflac.text import replace_spaces_with_pluses


async def set_correct_tags(directory: Path):
    # get artist and album tags
    tags = export_tags(directory)
    logger.debug(f"tags: {tags}")
    artist = get_tag(tags, "artist")
    album = get_tag(tags, "album")
    logger.debug(f"artist and album tags: {artist, album}")

    # make artist and album tags suitable for links
    artist_tag = replace_spaces_with_pluses(artist)
    album_tag = replace_spaces_with_pluses(album)
    logger.debug(f"artist and album tags for link: {artist_tag}, {album_tag}")

    # get album link from search query
    link_for_search = create_link_for_search(artist_tag, album_tag)
    logger.debug(f"link for search: {link_for_search}")
    search_content = fetch_page(link_for_search)
    album_link = get_album_link(search_content)
    logger.debug(f"album link: {album_link}")

    # get album page from album link
    if album_link is None:
        raise Exception("Album link is invalid")
    link_for_album_page = create_link_for_album_page(album_link)
    album_page = fetch_page(link_for_album_page)

    # get genres and date from album page
    genres = get_genres_from_album_page(album_page)
    date = get_date_from_album_page(album_page)
    date_object = datetime.strptime(date, "%B %d, %Y")
    formatted_date = date_object.strftime("%Y-%m-%d")

    # set tags
    set_tag(directory, "originaldate", formatted_date)
    set_tag(directory, "genre", genres)
