from flask import Flask, render_template, request, redirect, url_for, jsonify
import os
import requests
import base64
import pandas as pd


app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

adminUser = {"admin":"admin123"}

# Ana sayfa
@app.route('/')
def home():
    return render_template('index.html')

# Dosya seçme sayfası
@app.route('/choose')
def choose_page():
    return render_template('upload.html')

# Dosyaları yükleme sayfası
@app.route('/upload_page')
def upload_page():
    return render_template('upload_music.html')

# Dosya yükleme sayfası
@app.route('/admin_page', methods=["GET", "POST"])
def admin_page():
    error = None
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username in adminUser and adminUser[username] == password:
            return redirect(url_for("filter_page"))
        else:
            error = "Your username or password seems wrong. But you did not write wrong. We will give a chance for you. 🥺 👉👈 ＞﹏＜"
    
    return render_template('admin.html', error = error)


# Dosyaları yükleme endpoint'i
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'fileInput' not in request.files:
        return jsonify({'error': 'No file part'})

    file = request.files['fileInput']

    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    # Dosyaların yükleneceği klasörü kontrol et ve oluştur
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    # Dosyayı kaydet
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))

    # Dosya başarıyla yüklendikten sonra anasayfaya yönlendir
    return redirect(url_for('home'))



# Spotify API kimlik bilgileri
client_id = '0be9e7e75740419ba4782c57ea17b19b'
client_secret = '766748eb229b4470934df987a9089f99'

# Playlist URL
playlist_links = [
    "https://open.spotify.com/playlist/4vSTV61efRmetmaoz95Vet",
]

# Spotify API'ye kimlik doğrulaması
def get_access_token(client_id, client_secret):
    credentials = f"{client_id}:{client_secret}"
    base64_credentials = base64.b64encode(credentials.encode()).decode()

    auth_url = 'https://accounts.spotify.com/api/token'
    auth_data = {'grant_type': 'client_credentials'}
    auth_headers = {'Authorization': f'Basic {base64_credentials}'}
    auth_response = requests.post(auth_url, data=auth_data, headers=auth_headers)

    if auth_response.status_code == 200:
        auth_response_data = auth_response.json()
        access_token = auth_response_data['access_token']
        return access_token
    else:
        print(f"Kimlik doğrulama hatası: {auth_response.status_code}")
        return None

def get_playlist_tracks(access_token, playlist_urls):
    
    track_list = []

    for playlist_url in playlist_urls:
        playlist_id = playlist_url.split('/')[-1]
        playlist_tracks_url = f'https://api.spotify.com/v1/playlists/{playlist_id}/tracks'
        headers = {'Authorization': f'Bearer {access_token}'}
        playlist_tracks_response = requests.get(playlist_tracks_url, headers=headers)

        if playlist_tracks_response.status_code == 200:
            playlist_tracks_data = playlist_tracks_response.json()

            for item in playlist_tracks_data.get('items', []):
                track_info = item.get('track', {})
                artist_info = track_info['artists'][0] 
                artist_id = artist_info['id'] 

                artist_url = f'https://api.spotify.com/v1/artists/{artist_id}'
                artist_response = requests.get(artist_url, headers=headers)
                if artist_response.status_code == 200:
                    artist_data = artist_response.json()
                

                # Audio features bilgilerini çekiyoruz
                audio_features_url = f'https://api.spotify.com/v1/audio-features/{track_info["id"]}'
                audio_features_response = requests.get(audio_features_url, headers=headers)

                if audio_features_response.status_code == 200:
                    audio_features_data = audio_features_response.json()
                else:
                    print(f"Audio features bilgisi isteği hatası ({track_info['name']}): {audio_features_response.status_code}")
                    audio_features_data = {}

                track_list.append({
                    'Track Name': track_info.get('name', ''),
                    'Artist': artist_info.get('name', ''),
                    'Artist URI': artist_info.get('uri', ''),
                    'Artist Popularity': artist_data.get('popularity', 'N/A'),
                    'Artist Genres': ', '.join(artist_data.get('genres', [])),
                    'Release Date': track_info.get('album', {}).get('release_date', ''),
                    'Track Popularity': track_info.get('popularity', 'N/A'),
                    'Danceability': audio_features_data.get('danceability', ''),
                    'Energy': audio_features_data.get('energy', ''),
                    'Key': audio_features_data.get('key', ''),
                    'Loudness': audio_features_data.get('loudness', ''),
                    'Mode': audio_features_data.get('mode', ''),
                    'Speechiness': audio_features_data.get('speechiness', ''),
                    'Acousticness': audio_features_data.get('acousticness', ''),
                    'Instrumentalness': audio_features_data.get('instrumentalness', ''),
                    'Liveness': audio_features_data.get('liveness', ''),
                    'Valence': audio_features_data.get('valence', ''),
                    'Tempo': audio_features_data.get('tempo', ''),
                    'Type': audio_features_data.get('type', ''),
                    'Track ID': track_info.get('id', ''),
                    'Uri': track_info.get('uri', ''),
                    'Track_href': track_info.get('href', ''),
                    'Analysis_url': audio_features_data.get('analysis_url', ''),
                    'Duration_ms': track_info.get('duration_ms', ''),
                    'Time_signature': audio_features_data.get('time_signature', ''),
                })
        else:
            print(f"Playlist tracks isteği hatası ({playlist_url}): {playlist_tracks_response.status_code}")

    
    df = pd.DataFrame(track_list)
    return df
def filter_and_get_spotify_data(access_token, playlist_urls, filters):
    df = get_playlist_tracks(access_token, playlist_urls)

    
    for column, value in filters.items():
        if value:
            df = df[df[column].astype(str).str.contains(value, case=False, na=False)]

    return df

@app.route('/filter_page')
def filter_page():
    return render_template('filter.html')

@app.route('/filter_and_get_spotify_data', methods=['POST'])
def filter_and_get_spotify_data_endpoint():
    access_token = get_access_token(client_id, client_secret)

    if not access_token:
        return jsonify({'error': 'Invalid access token'})

    filters = request.get_json()
    df = filter_and_get_spotify_data(access_token, playlist_links, filters)
    print(df)

    
    json_data = df.to_json(orient='records')
    return json_data


if __name__ == '__main__':
    app.run(debug=True)