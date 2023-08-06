import os
import sys
import tty
import time
import termios
import argparse

import vlc
import pytube

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Set up the YouTube Data API v3 client
API_KEY = os.environ["YT_API_KEY"]
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'
youtube = build(YOUTUBE_API_SERVICE_NAME,
                YOUTUBE_API_VERSION, developerKey=API_KEY)


def get_video_urls(query, count=1):
    youtube = build(YOUTUBE_API_SERVICE_NAME,
                    YOUTUBE_API_VERSION, developerKey=API_KEY)
    request = youtube.search().list(
        part="id",
        q=query,
        type="video",
        videoDefinition="high",
        maxResults=count
    )
    response = request.execute()
    video_id = response['items'][0]['id']['videoId']
    return f"https://www.youtube.com/watch?v={video_id}"


def get_stream(video_url):
    video = pytube.YouTube(video_url)
    print(f'[{video.title}]')
    audio_stream = video.streams.filter(only_audio=True).first()
    return audio_stream


def get_player(audio_stream):

    # create a new instance of the vlc module with the --no-xlib argument
    args = ["--no-xlib", "--quiet", "--no-video"]
    instance = vlc.Instance(args)

    # create a media player with the new instance
    player = instance.media_player_new()

    # create a media object with the audio stream URL
    media = instance.media_new(audio_stream.url)

    player.set_media(media)
    return player


def main():
    parser = argparse.ArgumentParser(
        description='Listen to audio of YouTube videos from the command line.')
    parser.add_argument('query', nargs='+', help='search query for YouTube')
    args = parser.parse_args()

    # Get the search query from the command line arguments
    query = ' '.join(args.query).strip()

    # Save the terminal settings
    old_settings = termios.tcgetattr(sys.stdin)

    try:
        url = get_video_urls(query)
        audio_stream = get_stream(url)
        player = get_player(audio_stream)
        player.play()

        # Wait for the media to finish playing
        player_event_manager = player.event_manager()
        player_event_manager.event_attach(
            vlc.EventType.MediaPlayerEndReached, lambda _: player.stop())

        # Set the terminal to raw mode
        tty.setraw(sys.stdin.fileno())

        print('Press SPACE to pause. ENTER to quit.')
        while True:
            # Wait for 100 milliseconds
            time.sleep(0.5)

            # Wait for a single keypress
            key = sys.stdin.read(1)

            if key == ' ':
                player.pause()  # Pause the playback
            elif key == '\r':
                player.stop()  # Stop the playback
                break

    except IndexError as e:
        print("No media found. Try tweaking your search")

    except KeyboardInterrupt as e:
        # Handle keyboard interrupt gracefully
        player.stop()
        print("\nAudio playback stopped by the user.")

    except HttpError as e:
        print(f'An error occurred: {e}')

    except vlc.VLCException as e:
        print('Error', e)

    finally:
        # Restore the terminal settings
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)


if __name__ == "__main__":
    main()
