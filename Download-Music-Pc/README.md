# 🎵 Download-Music (.exe)

Aplicación de escritorio desarrollada en **Python** que permite descargar música desde YouTube en formato MP3 de manera sencilla.  
El proyecto fue empaquetado en un archivo ejecutable `.exe` para que funcione de forma portable en Windows.

---

## 🛠️ Herramientas y librerías utilizadas

- **Entorno controlado**: Virtualenv/Conda con **Python 3.10** para asegurar compatibilidad.  
- **Librerías principales**:
  - `yt-dlp` → Para descargar audio desde YouTube y otras plataformas.  
  - `ffmpeg` → Para convertir los archivos descargados a formato MP3 real.  
  - `kivy` → Para crear la interfaz gráfica multiplataforma.  

---

## 📋 Instalación (modo desarrollo)

1. Clona este repositorio:  
   ```bash
   git clone https://github.com/WAYwilsonlcc/Descargar-Musica.git
   cd Download-Music
   cd dist
        En `dist` se encuentra el archivo.exe listo para usar.