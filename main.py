import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth

"""
This program create a spotify playlist using top 100 tracks on Billboard on a specific date.
In order to access Spotify, go to https://developer.spotify.com/dashboard and login if already has an account
or create one.
Once create, get the Client ID and Client Secret which will be needed for authentication.
Add redirect_uri by editing settings.
P.S. Web scraping should be done ethically and don't forget to check website's rules.
"""

# Get the specific date from user.
date = input("Which year do you want to travel to?\n(Type the date in this format: yyyy-mm-dd)\n")
# Get the URL of the date provided.
URL = f"https://www.billboard.com/charts/hot-100/{date}"

# Use requests module to get hold the titles of the top 100 songs.
response = requests.get(URL)
soup = BeautifulSoup(response.text, "html.parser")
song_titles = [title.getText() for title in soup.find_all(name="span", class_="chart-element__information__song")]

# Access spotify for authentication.
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="YOUR_ID",
                                               client_secret="YOUR_SECRET",
                                               redirect_uri="http://example.com",
                                               scope="playlist-modify-private",
                                               show_dialog=True,
                                               cache_path="token.txt"))
# Get hold of user_ID of Spotify.
user_id = sp.current_user()["id"]
print(user_id)
# Get hold of the year only.
year = date.split("-")[0]
# Create an empty list to hold songs' URIs.
song_uris = []
# For every song in the list, search for URI in Spotify and append them to the created list.
for title in song_titles:
    result = sp.search(q=f"track:{title} year:{year}", type="track")
    print(result)
    # Check for errors, such as song doesn't exist in Spotify.
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{title} doesn't exist in Spotify. Skipped.")

# Create a playlist.
playlist = sp.user_playlist_create(user=user_id, name=f"{date} BillBoard 100", public=False)
print(playlist)
# Add songs that are available on Spotify to the created playlist.
sp.user_playlist_add_tracks(user=user_id, playlist_id=playlist["id"], tracks=song_uris)


