#!/usr/bin/env python3
import sys
import time
import random
import argparse

import vlc
import pafy
import youtube_dl

import playlist_fetcher

ytdl = None

def progress(count, total, status=''):
    bar_len = 60
    filled_len = int(round(bar_len * count / float(total)))

    percents = round(100.0 * count / float(total), 1)
    bar = '=' * filled_len + '-' * (bar_len - filled_len)

    sys.stdout.write(f'[{bar}] {percents}%\r')
    sys.stdout.flush()

def get_best_audio_url(json, verbose=False):
    for i in range(len(json['formats'])-1):
        if json['formats'][i+1].get('height') is not None:
            return json['formats'][i]['url']

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
        res = ytdl.extract_info(url, download=False)

        audio_url = get_best_audio_url(res)
        player = play_url(audio_url)

        sys.stdout.write('\033[K')
        while player.get_state() == vlc.State.Opening:
            time.sleep(1)

        print(res['title'])
        while player.get_state() != vlc.State.Ended:
            time.sleep(1)
            if player.get_length() != 0:
                sys.stdout.write('\033[K')
                progress(player.get_time(), player.get_length())


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

    ytdl = youtube_dl.YoutubeDL({
        'format': 'bestaudio',
        'quiet': not args.verbose}
    )

    if args.playlist is not None:
        #"https://www.youtube.com/playlist?list=PLNoB-hcIcvVd68WVqZGjWivuFgVgf5VVV"
        print('Fetching playlist...', end='\r')
        urls = playlist_fetcher.fetch(args.playlist, args.shuffle)
        play_url_list(urls)
