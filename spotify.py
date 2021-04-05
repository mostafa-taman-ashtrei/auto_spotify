import requests


class SpotifyClient:
    def __init__(self, token):
        self.token = token

    def search(self, artist, track):
        url = f'https://api.spotify.com/v1/search?query=track%3A{track}+artist%3A{artist}&type=track&offset=0&limit=20'

        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.token}'
        }

        res = requests.get(url, headers=headers)
        res_json = res.json()
        print(res.status_code)
        data = res_json['tracks']['items']

        if data:
            return data[0]['uri']
        else:
            raise Exception(f'No song found for {artist} named {track}')

    def song_exists(self, playlist_id):
        url = f'https://api.spotify.com/v1/playlists/{playlist_id}/tracks'
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.token}'
        }

        res = requests.get(url, headers=headers)
        res_json = res.json()
        existing_songs = []

        for x in res_json['items']:
            existing_songs.append(x['track']['uri'])

        return existing_songs

    def add_Song(self, playlist_id, song_uri):
        url = f'https://api.spotify.com/v1/playlists/{playlist_id}/tracks?uris={song_uri}'

        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.token}'
        }

        res = requests.post(url, headers=headers)
        print(res.json())
        return res.ok
