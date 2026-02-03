# Local
from filesystem import change_directory, delete_file
from tags import export_tags,
                 read_tags_from_file,
                 get_value_from_tag,
                 set_tag
from text import replace_spaces_with_pluses
from aoty_parsing import create_link,
                         fetch_page,
                         get_album_link,
                         get_genres_from_album_page,
                         get_year_from_album_page

TAGS_FILE="tags.txt"

def main(directory: str):
    # change directory
    change_directory(directory)

    # get artist and album tags
    export_tags(TAGS_FILE)
    tags = read_tags_from_file(TAGS_FILE)
    artist = get_value_from_tag(tags, "artist")
    album = get_value_from_tag(tags, "album")

    # make artist and album tags suitable for links
    artist_tag = replace_spaces_with_pluses(artist) 
    album_tag = replace_spaces_with_pluses(album)

    # get album link from search query
    link_for_search = create_link(artist_tag, album_tag)
    search_content = fetch_page(link_for_search)
    album_link = get_album_link(search_content)

    # get album page from album link
    link_for_album_page = create_link_for_album_page(album_link)
    album_page = fetch_page(link_for_album_page)

    # get genres and year from album page
    genres = get_genres_from_album_page(album_page)
    year = get_year_from_album_page(album_page)

    # set tags
    set_tag("date", year) 
    set_tag("genre", genres)

    # remove tags file
    delete_file(TAGS_FILE)
