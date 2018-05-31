#!/usr/bin/env python3

import sys
import urllib

from vlc import EventType
from PyQt5.QtWidgets import QWidget, QPushButton, QApplication, QLabel
from PyQt5.QtGui import QPixmap, QIcon

import playlist_fetcher
from ymp import YouTubePlayer

class Player(QWidget):
    def update_artwork(self, vlc_data, get_json_fun):
        json = get_json_fun()
        data = urllib.request.urlopen(json['thumbnail']).read()
        pixmap = QPixmap()
        pixmap.loadFromData(data)
        self.label.setPixmap(pixmap)
        self.label.repaint()

    def __init__(self):
        super().__init__()

        self.init_ui()

        self.yt_player = YouTubePlayer()
        self.yt_player.vlc_player.event_manager().event_attach(
            EventType.MediaPlayerPlaying, self.update_artwork, lambda: self.yt_player.current)
        self.yt_player.play_playlist('https://www.youtube.com/playlist?list=PLNoB-hcIcvVd68WVqZGjWivuFgVgf5VVV')


    def init_ui(self):
        playtoggle = QPushButton('Play', self)
        playtoggle.clicked.connect(lambda s: self.yt_player.vlc_player.pause())
        playtoggle.resize(playtoggle.sizeHint())
        playtoggle.move(350, 350)

        self.label = QLabel(self)
        self.label.setScaledContents(True)
        self.label.setGeometry(0, 0, 300, 300)

        self.setGeometry(300, 300, 700, 700)
        self.setWindowTitle('YouTube Media Player')
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Player()
    sys.exit(app.exec_())
