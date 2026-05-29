import threading
import os
import string
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.clock import Clock
from modules.downloader import download_audio

class DownloaderUI(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.output_dir = None 
        self._loading_event = None 

    def abrir_selector(self):
        drives = []
        if os.name == "nt":
            for letter in string.ascii_uppercase:
                drive = f"{letter}:\\"
                if os.path.exists(drive):
                    drives.append(drive)
            downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")
            if os.path.exists(downloads_path):
                drives.insert(0, downloads_path)
        else:
            drives = ["/"]

        chooser = FileChooserListView(path=drives[0], dirselect=True)

        spinner = Spinner(
            text=drives[0],
            values=drives,
            size_hint_y=None,
            height=40
        )

        def cambiar_unidad(spinner, text):
            chooser.path = text

        spinner.bind(text=cambiar_unidad)
        btn_ok = Button(text="Usar esta carpeta", size_hint_y=None, height=40)

        def confirmar(instance):
            self.output_dir = chooser.path
            self.ids.result_label.text = f"📂 Carpeta seleccionada:\n{self.output_dir}"
            popup.dismiss()
            self.descargar()

        btn_ok.bind(on_press=confirmar)

        btn_cancel = Button(text="Cancelar", size_hint_y=None, height=40)

        def cancelar(instance):
            self.output_dir = None
            self.ids.result_label.text = "Selección cancelada"
            popup.dismiss()

        btn_cancel.bind(on_press=cancelar)

        box = BoxLayout(orientation="vertical")
        box.add_widget(spinner)
        box.add_widget(chooser)

        btn_box = BoxLayout(orientation="horizontal", size_hint_y=None, height=40)
        btn_box.add_widget(btn_ok)
        btn_box.add_widget(btn_cancel)

        box.add_widget(btn_box)

        popup = Popup(title="Selecciona carpeta", content=box, size_hint=(0.9, 0.9))
        popup.open()

    def descargar(self):
        url = self.ids.url_input.text.strip()
        if not url:
            self.ids.result_label.text = "Debes ingresar una URL"
            return
        if not self.output_dir:
            self.ids.result_label.text = "Selecciona primero una carpeta"
            return

        self._start_loading_animation()

        threading.Thread(
            target=self._descargar_thread,
            args=(url,),
            daemon=True
        ).start()

    def _descargar_thread(self, url):
        resultado = download_audio(url, self.output_dir, update_ui=self._update_ui)
        self._update_ui(resultado)

    def _update_ui(self, mensaje):
        def update(dt):
            self._stop_loading_animation()
            self.ids.result_label.text = mensaje
        Clock.schedule_once(update)

    def _start_loading_animation(self):
        self.ids.result_label.text = "Cargando"
        self._loading_event = Clock.schedule_interval(self._animate_loading, 0.5)

    def _animate_loading(self, dt):
        text = self.ids.result_label.text
        if text.endswith("..."):
            self.ids.result_label.text = "Cargando"
        else:
            self.ids.result_label.text += "."

    def _stop_loading_animation(self):
        if self._loading_event:
            self._loading_event.cancel()
            self._loading_event = None
