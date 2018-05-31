import sys
import time
import random
import argparse
from pprint import pprint

import vlc
import pafy
import youtube_dl

def get_playlist_urls(playlist_url, verbose=False, shuffle=False):
    with youtube_dl.YoutubeDL({'format': 'bestaudio', 'quiet': not verbose}) as ytdl:
        r = ytdl.extract_info(playlist_url, download=False)

    urls = []
    for entry in r['entries']:
        for i in range(len(entry['formats'])):
            if entry['formats'][i+1].get('height') is not None:
                urls.append(entry['formats'][i]['url'])
                break

    return urls if not shuffle else random.shuffle(urls)

def play_url(url, volume=100):
    instance = vlc.Instance()
    player = instance.media_player_new()
    media = instance.media_new(url) 
    player.set_media(media)
    player.audio_set_volume(volume)
    player.play()

    return player

def play_url_list(url_list):
    for url in urls:
        player = play_url(url)

        sys.stdout.write('\033[K')
        print('Loading...\r', end='')
        while player.get_state() == vlc.State.Opening:
            time.sleep(1)

        while player.get_state() != vlc.State.Ended:
            time.sleep(1)
            sys.stdout.write('\033[K')
            print(f'{(player.get_time()/player.get_length())*100}%\r', end='')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='A program for streaming and managing YouTube audio')

    parser.add_argument('-p', '--playlist',
                        type=str,
                        help='url of the playlist to be played')

    parser.add_argument('-v', '--verbose',
                        default=False,
                        action='store_true',
                        help='displays additional output')

    parser.add_argument('-s', '--shuffle',
                        default=False,
                        action='store_true',
                        help='randomizes the order of the playlist')

    args = parser.parse_args()

    if args.playlist is not None:
        #"https://www.youtube.com/playlist?list=PLNoB-hcIcvVd68WVqZGjWivuFgVgf5VVV"
        urls = get_playlist_urls(args.playlist)
        play_url_list(urls)
