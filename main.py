from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner
import threading
import yt_dlp
import os

class DownloaderLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', padding=20, spacing=10, **kwargs)
        self.add_widget(Label(text='Video Downloader by Bin & Jack', font_size=20, size_hint_y=0.1))
        self.url_input = TextInput(hint_text='URL yahan paste karo...', multiline=False, size_hint_y=0.1)
        self.add_widget(self.url_input)
        self.quality = Spinner(text='Best Quality', values=('Best','720p','480p','360p','Audio MP3'), size_hint_y=0.1)
        self.add_widget(self.quality)
        btn = Button(text='Download Karo', size_hint_y=0.1, background_color=(0.2,0.6,1,1))
        btn.bind(on_press=self.start)
        self.add_widget(btn)
        self.status = Label(text='Ready...', size_hint_y=0.2)
        self.add_widget(self.status)

    def start(self, instance):
        url = self.url_input.text.strip()
        if not url:
            self.status.text = "Bhai URL toh daal!"
            return
        self.status.text = "Downloading..."
        threading.Thread(target=self.dl, args=(url,)).start()

    def dl(self, url):
        q = self.quality.text
        opts = {'outtmpl': '/sdcard/Download/%(title)s.%(ext)s', 'noplaylist': True}
        if q == 'Audio MP3':
            opts['format'] = 'bestaudio/best'
            opts['postprocessors'] = [{'key':'FFmpegExtractAudio','preferredcodec':'mp3'}]
        elif q == '720p':
            opts['format'] = 'bestvideo[height<=720]+bestaudio/best'
        elif q == '480p':
            opts['format'] = 'bestvideo[height<=480]+bestaudio/best'
        elif q == '360p':
            opts['format'] = 'bestvideo[height<=360]+bestaudio/best'
        else:
            opts['format'] = 'best'
        try:
            with yt_dlp.YoutubeDL(opts) as ydl:
                ydl.download([url])
            self.status.text = "Done! /sdcard/Download mein check karo"
        except Exception as e:
            self.status.text = "Error: " + str(e)

class DownloaderApp(App):
    def build(self):
        return DownloaderLayout()

if __name__ == '__main__':
    DownloaderApp().run()
