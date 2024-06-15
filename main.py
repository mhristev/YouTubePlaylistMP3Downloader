import os
from pytube import Playlist
from pytube import YouTube
from pydub import AudioSegment

def download_youtube_playlist(playlist_url, download_path='Downloads'):
    # Create the download directory if it doesn't exist
    if not os.path.exists(download_path):
        os.makedirs(download_path)

    # Load the playlist
    playlist = Playlist(playlist_url)
    print(f'Downloading playlist: {playlist.title}')

    for video_url in playlist.video_urls:
        try:
            print(f'Downloading video: {video_url}')
            yt = YouTube(video_url)
            video_title = yt.title
            video_stream = yt.streams.filter(only_audio=True).first()
            video_path = video_stream.download(output_path=download_path, filename=f'{video_title}.mp4')

            # Convert mp4 to mp3
            audio_path = os.path.join(download_path, f'{video_title}.mp3')
            AudioSegment.from_file(video_path).export(audio_path, format='mp3')

            # Optionally, you can remove the original video file
            os.remove(video_path)
            print(f'Converted and saved: {audio_path}')
        except Exception as e:
            print(f'Failed to download {video_url}: {e}')

if __name__ == '__main__':
    playlist_url = input('Enter the URL of the YouTube playlist: ')
    download_path = input('Enter the download path (default is "downloads"): ') or 'Downloads'
    download_youtube_playlist(playlist_url, download_path)
