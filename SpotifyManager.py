import spotipy
from spotipy.oauth2 import SpotifyOAuth


def setup_client():
    """Setups and returns the Spotipy client object"""

    # Method uses environment variables:
    # SPOTIPY_CLIENT_ID
    # SPOTIPY_CLIENT_SECRET
    # SPOTIPY_REDIRECT_URI

    scope = "playlist-read-private playlist-modify-private"
    am = SpotifyOAuth(
        scope=scope,
        open_browser=False
    )

    return spotipy.Spotify(auth_manager=am)


class SpotifyManager:

    def __init__(self, date):
        self.client = setup_client()
        self.date = date
        self.playlist_name = f"Billboard Top100"

    def get_user_id(self):
        """Used to return the current user ID"""
        return self.client.current_user()["id"]

    def get_song_uri(self, song):
        """Gets the Spotify URI of the current song. Returns URI or None if song not found"""

        result = self.client.search(
            q=f"track:{song} year:{self.date[:4:]}",  # Spotify query with the song name and a
            # year (made by slicing first 4 digits of the date)
            type="track",
            limit=1
        )

        # Checks if it is possible to get URI from the search results
        try:
            uri = result["tracks"]["items"][0]["uri"]
            return uri
        except IndexError:
            pass

    def check_playlist(self):
        """Checks if current user has a playlist with the name '{date} - Billboard Top100'. If the playlist exists then
        removes it."""
        playlists = self.client.current_user_playlists()
        for playlist in playlists["items"]:
            p_name = playlist["name"]
            if p_name == self.playlist_name:
                pl_id = playlist["id"]
                self.client.current_user_unfollow_playlist(pl_id)

    def create_playlist(self, tracks):
        """Creates a playlist with the name '{date} - Billboard Top100' and adds the tracks from the list to it"""
        self.check_playlist()
        playlist = self.client.user_playlist_create(
            user=self.get_user_id(),
            public=False,
            name=self.playlist_name
        )
        pl_id = playlist["id"]

        self.client.playlist_add_items(
            playlist_id=pl_id,
            items=tracks
        )
        return playlist
