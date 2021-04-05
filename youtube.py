import os
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
import youtube_dl


class YoutubeClient:
    def __init__(self):
        creds_json = 'creds.json'
        scopes = ['https://www.googleapis.com/auth/youtube.readonly']
        credentials = None
        pickle_file = 'tokens.pickle'
        api_service_name = 'youtube'
        api_version = 'v3'

        if os.path.exists(pickle_file):
            print('Fetching tokens from pickle file')
            with open(pickle_file, 'rb') as f:
                credentials = pickle.load(f)

        if not credentials or not credentials.valid:
            if credentials and credentials.expired and credentials.refresh_token:
                print('Refresing token ...')
                credentials.refresh(Request())
            else:
                print('Fetching new tokens ...')

                flow = InstalledAppFlow.from_client_secrets_file(
                    creds_json,
                    scopes=scopes
                )

                flow.run_local_server(
                    host='localhost',
                    port=8080,
                    prompt='consent',
                    authorization_prompt_message=''
                )

                credentials = flow.credentials
                print(credentials.to_json())

                with open(pickle_file, 'wb') as f:
                    print('Saving tokens to pickle file ...')
                    pickle.dump(credentials, f)

        self.client = build(api_service_name, api_version,
                            credentials=credentials)

    def get_playlists(self):
        req = self.client.playlists().list(
            part='id, snippet',
            mine=True
        )

        res = req.execute()
        my_playlists = [{'id': item['id'], 'name': item['snippet']['title']}
                        for item in res['items']]

        print(my_playlists)
        return my_playlists

    def get_videos(self, playlist_id):
        my_songs = []

        req = self.client.playlistItems().list(
            playlistId=playlist_id, part='id, snippet')

        res = req.execute()
        for item in res['items']:
            video_id = item['snippet']['resourceId']['videoId']
            print(video_id)
            artist, track = self.get_video_artist_and_track(video_id)

            if artist is not None and track is not None:
                my_songs.append({'artist': artist, 'track': track})

        print(my_songs)
        return my_songs

    def get_video_artist_and_track(self, video_id):
        youtube_url = f'https://www.youtube.com/watch?v={video_id}'

        video = youtube_dl.YoutubeDL({}).extract_info(
            youtube_url, download=False)

        if 'track' in video.keys() and 'artist' in video.keys():
            track = video['track']
            artist = video['artist']
        else:
            artist = None
            track = None

        return artist, track
