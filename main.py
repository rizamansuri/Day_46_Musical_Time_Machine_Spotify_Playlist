import os
from pprint import pprint
import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth

date = input("Which year you want to travel to? Type the date in this format YYYY-MM-DD:")
URL = "https://www.billboard.com/charts/hot-100"

response = requests.get(f"{URL}/{date}")
top_songs_web_data = response.text

soup = BeautifulSoup(top_songs_web_data, "html.parser")
song_list = soup.select(selector="li ul li h3")
song_list = [song.getText().strip() for song in song_list]
# print(song_list)

CLIENT_ID = os.environ.get("CLIENT_ID")
CLIENT_SECRET = os.environ.get("CLIENT_SECRET")
REDIRECT_URL = "http://example.com"

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        show_dialog=True,
        cache_path="token.txt",
        username="RIZA",
    )
)
user_id = sp.current_user()["id"]
song_uris = []
playlist_name = f"{date} Billboard 100"
song_year = date.split('-')[0]

for song in song_list:
    searchResults = sp.search(q=f"track: {song} year: {song_year}", limit=1, type='track')
    try:
        uri = searchResults['tracks']['items'][0]['uri']
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")
pprint(song_uris)
playlist = sp.user_playlist_create(user=user_id, name=playlist_name, public=False)
# pprint(playlist)


try:
    # Adding songs found into the new playlist
    sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)
except Exception:
    print(Exception)

