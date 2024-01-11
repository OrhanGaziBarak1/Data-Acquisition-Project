from flask import Flask, render_template, request, jsonify
import requests
import base64
import csv
import time
import pandas as pd


app = Flask(__name__)

# Spotify API kimlik bilgileri
client_id = '809a46219b4a48ab8bcb5fb19772cc98'
client_secret = 'e2ab7793e76c4dd1a0b43ebb3c5a5a18'

# Playlist URL'lerini tanımlıyoruz.
playlist_links = [
    "https://open.spotify.com/playlist/4vSTV61efRmetmaoz95Vet",
]

# Spotify API'ye kimlik doğrulaması yapmak için gerekli olan erişim anahtarını alır
def get_access_token(client_id, client_secret):
    credentials = f"{client_id}:{client_secret}"
    base64_credentials = base64.b64encode(credentials.encode()).decode()

    auth_url = 'https://accounts.spotify.com/api/token'
    auth_data = {
        'grant_type': 'client_credentials',
    }
    auth_headers = {
        'Authorization': f'Basic {base64_credentials}',
    }
    auth_response = requests.post(auth_url, data=auth_data, headers=auth_headers)

    if auth_response.status_code == 200:
        auth_response_data = auth_response.json()
        access_token = auth_response_data['access_token']
        return access_token
    else:
        print(f"Kimlik doğrulama hatası: {auth_response.status_code}")
        return None

def get_playlist_tracks(access_token, playlist_url, csv_writer):
    # Playlist ID'sini çıkarıyoruz.
    playlist_id = playlist_url.split('/')[-1]

    playlist_tracks_url = f'https://api.spotify.com/v1/playlists/{playlist_id}/tracks'
    headers = {
        'Authorization': f'Bearer {access_token}',
    }
    playlist_tracks_response = requests.get(playlist_tracks_url, headers=headers)

    if playlist_tracks_response.status_code == 200:
        playlist_tracks_data = playlist_tracks_response.json()
        for item in playlist_tracks_data['items']:
            track_info = item['track']
            track_id = track_info['id']
            
            # Audio features bilgilerini çekiyoruz.
            audio_features_url = f'https://api.spotify.com/v1/audio-features/{track_id}'
            time.sleep(0.1)
            audio_features_response = requests.get(audio_features_url, headers=headers)
            
            if audio_features_response.status_code == 200:
                audio_features_data = audio_features_response.json()
                
                # Artist bilgilerini çekiyoruz.
                artist_info = track_info['artists'][0]  
                artist_id = artist_info['id']
                artist_url = f'https://api.spotify.com/v1/artists/{artist_id}'
                artist_response = requests.get(artist_url, headers=headers)
                
                if artist_response.status_code == 200:
                    artist_data = artist_response.json()
                    artist_genres = ', '.join(artist_data.get('genres', [])) 

                    
                    artist_popularity = artist_data.get('popularity', 'N/A')

                    # Tüm bilgileri çekiyoruz
                    row = [track_info['name'], artist_info['name'], artist_info['uri'], artist_popularity, artist_genres,
                     track_info['album']['release_date'], track_info['popularity']]
                    row.extend(list(audio_features_data.values()))
                    
                    csv_writer.writerow(row)
                else:
                    print(f"Artist bilgisi isteği hatası: {artist_response.status_code}")
            else:
                print(f"Audio features bilgisi isteği hatası: {audio_features_response.status_code}")

# CSV dosyasını aç ve başlık satırını yazıyoruz.
def write_csv_file():
    with open('playlist_dataset.csv', 'w', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)
        header = ['Track Name', 'Artist', 'Artist URI', 'Artist Popularity', 'Artist Genres', 'Release Date', 'Track Popularity']
        header.extend(['Danceability', 'Energy', 'Key', 'Loudness', 'Mode', 'Speechiness', 'Acousticness',
                    'Instrumentalness', 'Liveness', 'Valence', 'Tempo', 'Type','Track ID', 'Uri', 'Track_href', 'Analysis_url', 'Duration_ms', 'Time_signature'])
        csv_writer.writerow(header)

        # Her bir playlist için veri çekme ve CSV dosyasına yazma işlemleri
        for playlist_link in playlist_links:
            access_token = get_access_token(client_id, client_secret)
            get_playlist_tracks(access_token, playlist_link, csv_writer)


# Musixmatch API anahtarı
api_key = "a8ff8b325ae61386fe443091b21ff478"

# Musixmatch API kullanarak şarkı ID'sini alıyoruz.
def get_track_id(api_key, track_name, artist_name):
    url = f"https://api.musixmatch.com/ws/1.1/track.search?q_track={track_name}&q_artist={artist_name}&apikey={api_key}"
    response = requests.get(url)
    data = response.json()

    if data["message"]["header"]["status_code"] == 200:
        track_list = data["message"]["body"]["track_list"]
        if track_list:
            track_id = track_list[0]["track"]["track_id"]
            return track_id
        else:
            print(f"{artist_name} tarafından {track_name} bulunamadı.")
            return None
    else:
        print(f"{artist_name} tarafından {track_name} için track ID alınırken hata oluştu: {data['message']['header']['status_code']}")
        return None

# Musixmatch API kullanarak şarkı sözlerini alıyoruz.
def get_lyrics(api_key, track_id):
    url = f"https://api.musixmatch.com/ws/1.1/track.lyrics.get?track_id={track_id}&apikey={api_key}"
    response = requests.get(url)
    data = response.json()

    if data["message"]["header"]["status_code"] == 200:
        lyrics = data["message"]["body"]["lyrics"]["lyrics_body"]
        return lyrics
    else:
        return None

# CSV dosyasını aç ve başlık satırını yazıyoruz.
input_csv_path = 'playlist_dataset.csv'  # Bu dosyayı kendi CSV dosyanızın adıyla değiştiriyoruz.
output_csv_path = 'final_dataset.csv'  # Çıktı dosyasının adını belirtiyoruz.

with open(input_csv_path, 'r', newline='', encoding='utf-8') as input_csv, \
        open(output_csv_path, 'w', newline='', encoding='utf-8') as output_csv:
    
    # Giriş ve çıkış CSV dosyaları için okuma ve yazma nesnelerini oluşturuyoruz.
    input_reader = csv.DictReader(input_csv)
    fieldnames = input_reader.fieldnames + ['Lyrics']  # Yeni sütunu ekliyoruz

    output_writer = csv.DictWriter(output_csv, fieldnames=fieldnames)
    output_writer.writeheader()

    for row in input_reader:
        track_name = row['Track Name']
        artist_name = row['Artist']

        # Track ID'yi alıyoruz.
        track_id = get_track_id(api_key, track_name, artist_name)

        if track_id:
            # Lyrics'i alıyoruz.
            lyrics = get_lyrics(api_key, track_id)

            # Yeni sütunu ekleyip yazıyoruz.
            row['Lyrics'] = lyrics
            output_writer.writerow(row)

# CSV dosyasını oluşturmak için /download_csv endpoint'i
@app.route('/download_csv', methods=['GET'])
def download_csv():
    write_csv_file()
    return jsonify({'message': 'CSV file created successfully'})

# Ana sayfa için route
@app.route('/')
def home():
    return render_template('filter.html')

# Spotify verilerini filtreleme için /filter_and_get_spotify_data endpoint'i
@app.route('/filter_and_get_spotify_data', methods=['POST'])
def filter_and_get_spotify_data():
    filters = request.get_json()

    
    df = pd.read_csv('playlist_dataset.csv')

    # Filtreleme işlemlerini uyguluyoruz.
    for column, value in filters.items():
        if value:
            if isinstance(df[column].iloc[0], str):
                df = df[df[column].str.contains(value, case=False, na=False)]
            elif isinstance(df[column].iloc[0], int):
                df = df[df[column].astype(str).str.contains(value, case=False, na=False)]

    
    return jsonify(df.to_dict(orient='records'))

if __name__ == "__main__":
    app.run(debug=True)