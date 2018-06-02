#!/usr/bin/env python3
import sys
import time
import random
import argparse
import threading
from pprint import pprint

import vlc
import pafy
import youtube_dl

import playlist_fetcher
from loggers import Logger, StdLogger

class YouTubePlayer:
    def __init__(self, verbose=False):
        self.ytdl = youtube_dl.YoutubeDL({
            'format': 'bestaudio',
            'quiet': not verbose
            }
        )
        self.logger = StdLogger() if verbose else Logger()
        self.vlc_instance = vlc.Instance()
        self.vlc_player = self.vlc_instance.media_player_new()
        self.current = None
        self.queue = None

    def get_best_audio_url(self, json, verbose=False):
        self.logger.info('Fetching best url')
        for i in range(len(json['formats'])-1):
            if json['formats'][i+1].get('height') is not None:
                return json['formats'][i]['url']

    def play_url(self, json, audio_url, volume=100):
        media = self.vlc_instance.media_new(audio_url) 
        self.vlc_player.set_media(media)
        self.vlc_player.audio_set_volume(volume)
        self.logger.info('Playing song')
        self.vlc_player.play()
        self.vlc_player.set_time(self.vlc_player.get_length() - 10000)
        self.current = json

    def song_finished_callback(self, data, url_iterator):
        self.logger.info('Song completed callback reached')
        t = threading.Thread(target=self.play_url_list, args=(url_iterator, True))
        t.start()

    def play_url_list(self, url_iterator, recursive=False):
        nxt = next(url_iterator)
        self.logger.info(f"Extracting info for '{nxt}'")
        res = self.ytdl.extract_info(nxt, download=False)

        audio_url = self.get_best_audio_url(res)
        print(audio_url)
        self.play_url(res, audio_url)

        while self.vlc_player.get_state() == vlc.State.Opening:
            time.sleep(1)

        if not recursive:
            events = self.vlc_player.event_manager()
            events.event_attach(vlc.EventType.MediaPlayerEndReached, self.song_finished_callback, url_iterator)

    def play_playlist(self, playlist_url, shuffle=False):
        self.logger.info('Fetching url... ', end='')
        self.queue = playlist_fetcher.fetch(playlist_url)
        self.play_url_list(self.queue)

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

    #"https://www.youtube.com/playlist?list=PLNoB-hcIcvVd68WVqZGjWivuFgVgf5VVV"
    if args.playlist is None:
        exit(0)

    c = YouTubePlayer(verbose=args.verbose)
    c.play_playlist(args.playlist, args.shuffle)

    while 1:
       time.sleep(1)
       if c.vlc_player.get_length() != 0:
           print(f'{c.current["title"]} - {(c.vlc_player.get_time()/c.vlc_player.get_length())*100:.2f}%')
