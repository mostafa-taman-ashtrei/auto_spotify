from youtube import YoutubeClient
from spotify import SpotifyClient


def main():
    youtube_client = YoutubeClient()
    spotify_client = SpotifyClient()

    playlists = youtube_client.get_playlists()

    music_playlist = [
        playlist for playlist in playlists if playlist['name'] == 'music'
    ]
    music_playlist_id = music_playlist[0]['id']
    my_songs = youtube_client.get_videos(music_playlist_id)


if __name__ == '__main__':
    main()
