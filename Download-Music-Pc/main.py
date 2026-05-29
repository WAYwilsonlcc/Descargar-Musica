import os
import sys
from kivy.app import App
from kivy.lang import Builder
from ui.home import DownloaderUI

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class DownloadMusicApp(App):
    def build(self):
        Builder.load_file(resource_path("home.kv"))
        return DownloaderUI()

if __name__ == "__main__":
    DownloadMusicApp().run()
