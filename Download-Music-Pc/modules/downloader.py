import yt_dlp
import os
import re

def download_audio(url: str, output_dir: str, update_ui=None) -> str:
    patron = re.compile(r'^https?://[^\s]+$')

    class MyLogger:
        def debug(self, msg): 
            pass
        def warning(self, msg): 
            pass
        def error(self, msg): 
            if update_ui:
                update_ui(f"Advertencia {msg}")

    def my_hook(d):
        if d['status'] == 'downloading' and update_ui:
            percent = d.get('_percent_str', '').strip()
            update_ui(f"Descargando... {percent}")
        elif d['status'] == 'finished' and update_ui:
            update_ui("Conversión a MP3...")

    match url:
        case u if not u:
            return "La URL está vacía"
        case u if not patron.match(u):
            return "La URL no es válida"
        case u if "youtube.com" in u or "youtu.be" in u:
            os.makedirs(output_dir, exist_ok=True)

            ydl_opts = {
                "format": "bestaudio/best",
                "outtmpl": os.path.join(output_dir, "%(title)s.%(ext)s"),
                "logger": MyLogger(),
                "progress_hooks": [my_hook],
                "postprocessors": [{
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "192",
                }],
                "ffmpeg_location": os.path.join(os.path.dirname(__file__), "..", "bin"),
            }
            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])
                return "Descarga completada"
            except Exception as e:
                return f"Error al descargar: {e}"
        case _:
            return "Es una URL válida, pero no reconocida"
