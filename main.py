import datetime

import requests
from bs4 import BeautifulSoup

from SpotifyManager import SpotifyManager

BASE_URL = "https://www.billboard.com/charts/hot-100/"


def check_date(dt):
    """Checks if the input date_check complies with the predefined format (YYYY-MM-DD) and is not in the future. Returns
    True if all checks passed"""
    try:
        date_check = datetime.datetime.strptime(dt, '%Y-%m-%d').date()
    except ValueError:
        print("There is an error in the date_check. Should be of format YYYY-MM-DD.")
        return False
    else:
        if date_check > datetime.datetime.now().date():
            print("The date_check should not be in the future")
            return False
        else:
            return True


# Asks a user to input a date. The date must be valid and not in the future
is_date_correct = False

while not is_date_correct:
    date = input("Which year do you want to travel to? Type the date_in in format YYYY-MM-DD. ")
    is_date_correct = check_date(date)

# Uses the requests library to get the HTML from Billboard Top100 on the specified date
response = requests.get(BASE_URL + date)
response.raise_for_status()

# Uses Beautiful Soup to scrap song title from the HTML page and compile them as a list
soup = BeautifulSoup(response.text, "html.parser")
song_title_tags = soup.find_all(name="span", class_="chart-element__information__song")
songs = [tag.getText() for tag in song_title_tags]

# Initialises the custom class SpotifyManager with the date (see description in the class itself)
sm = SpotifyManager(date)

# Uses list comprehension to make a list of song URIs ("if" statement checks if the element in the list exists -
# method get_song_uri car return None if there is no such song on Spotify)
track_URIs = [sm.get_song_uri(song) for song in songs if sm.get_song_uri(song)]

# Creates the playlist with songs from previous step
sm.create_playlist(tracks=track_URIs)
