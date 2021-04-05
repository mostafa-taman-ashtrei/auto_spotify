import os
from dotenv import load_dotenv

from youtube import YoutubeClient
from spotify import SpotifyClient

load_dotenv()


def main():
    youtube_client = YoutubeClient()
    spotify_client = SpotifyClient(os.getenv('SPOTFY_TOKEN'))

    playlists = youtube_client.get_playlists()

    music_playlist = [
        playlist for playlist in playlists if playlist['name'] == 'spotify'
    ]
    music_playlist_id = music_playlist[0]['id']
    my_songs = youtube_client.get_videos(music_playlist_id)

    spotify_playlist_id = '3I5aRuFgAvZ4eiELHV11Zo'
    existing_songs = spotify_client.song_exists(spotify_playlist_id)

    for song in my_songs:
        song_uri = spotify_client.search(song['artist'], song['track'])

        if song_uri:
            if song_uri in existing_songs:
                print(f'{song_uri} already exists')
            else:
                added_song = spotify_client.add_Song(
                    spotify_playlist_id, song_uri)
                print(added_song)
                if added_song:
                    print(f'{song_uri} has been added to your playlist')


if __name__ == '__main__':
    main()
