from datetime import datetime,timedelta
import requests
from bs4 import BeautifulSoup
from UserManager import UserManager
from NotificationManager import NotificationManager

from SpotifyManager import SpotifyManager

BASE_URL = "https://www.billboard.com/charts/hot-100/"

# Gets the yesterday date
dt = datetime.now() - timedelta(days=1)
date = str(dt.date())


# Uses the requests library to get the HTML from Billboard Top100 on the specified date
response = requests.get(BASE_URL + date)
response.raise_for_status()

# Uses Beautiful Soup to scrap song title from the HTML page and compile them as a list
soup = BeautifulSoup(response.text, "html.parser")
song_title_tags = soup.find_all(name="span", class_="chart-element__information__song")
songs = [tag.getText() for tag in song_title_tags]

# Initialises the custom class SpotifyManager with the date (see description in the class itself)
sm = SpotifyManager(date)

# Gets the list of users from the subscribers Google Sheet
um = UserManager()
users = um.get_users()

# Uses list comprehension to make a list of song URIs ("if" statement checks if the element in the list exists -
# method get_song_uri car return None if there is no such song on Spotify)
track_URIs = [sm.get_song_uri(song) for song in songs if sm.get_song_uri(song)]

# Creates the playlist with songs from previous step
playlist = sm.create_playlist(tracks=track_URIs)

# Initialize Nmtification Manager with the current playlist
nm = NotificationManager(playlist)

# Send e-mails to all subscribed users
for user in users:
    nm.send_email(user)
