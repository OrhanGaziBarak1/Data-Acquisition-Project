import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Spotify API istemci kimlik bilgileri
client_id = '809a46219b4a48ab8bcb5fb19772cc98'
client_secret = 'e2ab7793e76c4dd1a0b43ebb3c5a5a18'

# Spotify API'ye erişim sağlamak için kimlik doğrulama yöntemini kullan
client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# 7 farklı playlist linkini içeren bir liste
playlist_links = [
    "https://open.spotify.com/playlist/37i9dQZF1DWTNZTmARWKQa?si=sCfabRNrTpaYUOfpCPltbg&pi=e-tkJv8HOGS_ej&nd=1&dlsi=fb1ec568be9a46ff",
    "https://open.spotify.com/playlist/1e7u35nUdO3GxSAc4tBGu2?si=4isDYKOuRdW99CLX2Kb3-g&pi=e-8tV-0yYDRIit&nd=1&dlsi=31b6e7bafd8e4048",
    "https://open.spotify.com/playlist/3etNjGlQTQRurDDVhM68J8?si=feIyr29xTUuOXGD5Q6UvSA&pi=e-E2IA0cg6QYyT&nd=1&dlsi=007fd7e54cf84bfe",
    "https://open.spotify.com/playlist/2znNvGyQxAUmp6cdX4uM1o?si=Ovx8XAMPQ3yV7c-qsWOrkQ&pi=e-NuY53AEeQ5uP&nd=1&dlsi=cbbe21bba1ff4bc2",
]

# Her bir playlist için işlemi tekrarla
for playlist_link in playlist_links:
    # Playlist URI'sini al
    playlist_URI = playlist_link.split("/")[-1].split("?")[0]

    # Playlist'teki şarkıları yazdır
    print(f"Playlist: {playlist_link}")
    for track in sp.playlist_tracks(playlist_URI)["items"]:
        # To get track URI
        track_uri = track["track"]["uri"]

        # To get track name
        track_name = track["track"]["name"]

        # To get main artist
        artist_uri = track["track"]["artists"][0]["uri"]
        artist_info = sp.artist(artist_uri)

        # To get arist information
        artist_name = track["track"]["artists"][0]["name"]
        artist_pop = artist_info["popularity"]
        artist_genres = artist_info["genres"]
        
        # To get album name
        album = track["track"]["album"]["name"]

        # For popularity of the track
        track_pop = track["track"]["popularity"]
        
        # Verileri yazdır
        print(f"Track: {track_name}")
        print(f"   - URI: {track_uri}")
        print(f"   - Artist: {artist_name}")
        print(f"   - Artist URI: {artist_uri}")
        print(f"   - Artist Popularity: {artist_pop}")
        print(f"   - Artist Genres: {', '.join(artist_genres)}")
        print(f"   - Album: {album}")
        print(f"   - Track Popularity: {track_pop}")
        print("\n")
