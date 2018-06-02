#!/usr/bin/env python3

import sys
import types
import urllib

from vlc import EventType
from PyQt5.QtWidgets import QWidget, QPushButton, QApplication, QLabel
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import pyqtSignal

import playlist_fetcher
from ymp import YouTubePlayer

class Player(QWidget):
    def update_artwork(self, json):
        data = urllib.request.urlopen(json['thumbnail']).read()
        pixmap = QPixmap()
        pixmap.loadFromData(data)
        self.label.setPixmap(pixmap)
        self.label.repaint()

    album_updated = pyqtSignal(dict, name='album_art_updated')

    def __init__(self):
        super().__init__()

        self.init_ui()

        self.album_updated.connect(self.update_artwork)

        self.yt_player = YouTubePlayer()
        self.yt_player.vlc_player.event_manager().event_attach(
            EventType.MediaPlayerPlaying, lambda d: self.album_updated.emit(self.yt_player.current))
        
        self.yt_player.play_playlist('https://www.youtube.com/playlist?list=PLNoB-hcIcvVd68WVqZGjWivuFgVgf5VVV')


    def init_ui(self):
        playtoggle = QPushButton('Play', self)
        playtoggle.clicked.connect(lambda s: self.yt_player.vlc_player.pause())
        playtoggle.resize(playtoggle.sizeHint())
        playtoggle.move(0, 340)

        self.label = QLabel(self)
        self.label.setScaledContents(True)
        self.label.setGeometry(0, 0, 600, 338)

        self.setGeometry(300, 300, 700, 700)
        self.setWindowTitle('YouTube Media Player')
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Player()
    sys.exit(app.exec_())
