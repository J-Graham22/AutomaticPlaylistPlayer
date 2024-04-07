import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json
from datetime import datetime
from time import sleep

client_id = 'CLIENT_ID'
client_secret = 'CLIENT_SECRET'
redirect_uri = 'REDIRECT_URI'
playlist_id = 'PLAYLIST_ID' #wake uplist
device_id = 'DEVICE_ID' #computer
times_to_start = ''

def main():
    read_json_values()
    sp_client = setup_spotify()

    while True:
        now = datetime.now()
        time_string = now.strftime("%I:%M %p")

        for time in times_to_start:
            if time == time_string:
                play_playlist(sp_client)
                break

        sleep(60 - now.second)

def read_json_values():
    global client_id, client_secret, redirect_uri, playlist_id, device_id, times_to_start
    file = open('values.json')
    data = json.load(file)

    client_id = data['client_id']
    client_secret = data['client_secret']
    redirect_uri = data['redirect_uri']
    playlist_id = data['playlist_id']
    device_id = data['device_id']
    times_to_start = data['times_to_start']

def setup_spotify():
    sp_client = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri, scope='user-library-read playlist-read-private user-modify-playback-state user-read-playback-state'))
    sp_client.shuffle(False, device_id)
    return sp_client

def play_playlist(sp_client):
    playlist = sp_client.playlist(playlist_id=playlist_id)
    print(f"Playing {playlist['name']}...")
    sp_client.start_playback(device_id=device_id, context_uri=f'spotify:playlist:{playlist_id}')

if __name__ == '__main__':
    main()