from dotenv import load_dotenv
import os
import base64
import json
import re
from requests import post, get
import requests

load_dotenv()

# Spotify API credentials
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

# Musixmatch API key
musixmatch_api_key = os.getenv("MUSIXMATCH_API_KEY")

def get_token():
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}
    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    return token

def get_auth_header(token):
    return {"Authorization": "Bearer " + token}

def get_spotify_playlist_info(playlist_url):
    # Spotify playlist URL'sinden playlist ID'sini çıkarma
    playlist_id = re.search(r'playlist\/(\w+)', playlist_url).group(1)

    # Spotify API'ı için token al
    token = get_token()

    # Playlist bilgilerini al
    playlist_info = get_playlist_info(token, playlist_id)

    if playlist_info:
        print(f"Playlist Name: {playlist_info['name']}")
        print("Tracks:")
        for idx, track in enumerate(playlist_info['tracks']):
            print(f"{idx + 1}. {track['name']}")
            print(f"   Artists: {', '.join(artist['name'] for artist in track['artists'])}")
            print(f"   Genres: {', '.join(get_track_genres(token, track['id']))}")
            print(f"   Popularity: {track['popularity']}")
            print(f"   Track URI: {track['uri']}")

            # Get lyrics for the track
            lyrics = get_lyrics(track['name'], track['artists'][0]['name'])
            if lyrics:
                print(f"   Lyrics: {lyrics}")
            else:
                print("   Lyrics not found")

            print("\n")
    else:
        print("Playlist not found.")

def get_playlist_info(token, playlist_id):
    # Spotify API üzerinden çalma listesi bilgilerini al
    url = f"https://api.spotify.com/v1/playlists/{playlist_id}"
    headers = {"Authorization": "Bearer " + token}
    
    result = requests.get(url, headers=headers)
    if result.status_code == 200:
        playlist_info = result.json()
        return {
            "name": playlist_info["name"],
            "tracks": [{
                "name": track["track"]["name"],
                "artists": track["track"]["artists"],
                "id": track["track"]["id"],
                "popularity": track["track"]["popularity"],
                "uri": track["track"]["uri"]
            } for track in playlist_info["tracks"]["items"]]
        }
    else:
        print(f"Error getting playlist info: {result.status_code}")
        return None
    

def get_track_genres(token, track_id):
    # Spotify API üzerinden şarkının türlerini al
    url = f"https://api.spotify.com/v1/tracks/{track_id}"
    headers = {"Authorization": "Bearer " + token}

    result = requests.get(url, headers=headers)
    if result.status_code == 200:
        track_info = result.json()
        # Sanatçının türlerini al
        artist_genres = get_artist_genres(token, track_info["artists"][0]["id"])
        return artist_genres
    else:
        print(f"Error getting track genres: {result.status_code}")
        return []

def get_artist_genres(token, artist_id):
    # Spotify API üzerinden sanatçının türlerini al
    url = f"https://api.spotify.com/v1/artists/{artist_id}"
    headers = {"Authorization": "Bearer " + token}

    result = requests.get(url, headers=headers)
    if result.status_code == 200:
        artist_info = result.json()
        # Sanatçının türlerini al
        artist_genres = artist_info.get("genres", [])
        return artist_genres
    else:
        print(f"Error getting artist genres: {result.status_code}")
        return []


def get_lyrics(track_name, artist_name):
    # Musixmatch API for getting lyrics
    url = "https://api.musixmatch.com/ws/1.1/matcher.lyrics.get"
    params = {
        "format": "json",
        "q_track": track_name,
        "q_artist": artist_name,
        "apikey": musixmatch_api_key
    }

    result = requests.get(url, params=params)
    if result.status_code == 200:
        lyrics_info = result.json().get("message", {}).get("body", {}).get("lyrics", {})
        return lyrics_info.get("lyrics_body", "")
    else:
        print(f"Error getting lyrics: {result.status_code}")
        return None

# Kullanıcıdan Spotify çalma listesi URL'sini al
playlist_url = input("Enter Spotify Playlist URL: ")
get_spotify_playlist_info(playlist_url)
