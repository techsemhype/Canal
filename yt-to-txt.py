#!/Users/db/Downloads/venv/bin/python3
import os
import argparse
import whisper
import yt_dlp

# Diretório de destino para salvar os arquivos
DOWNLOAD_DIR = os.path.expanduser("~/Downloads")

def download_audio(url):
    ydl_opts = {
        "format": "bestaudio/best",
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }
        ],
        "outtmpl": os.path.join(DOWNLOAD_DIR, "%(title)s.%(ext)s"),
        "keepvideo": False,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        title = info.get('title', 'audio')
        upload_date = info.get('upload_date', '00000000')

        # Busca o arquivo MP3 real criado (pode ter nome sanitizado)
        base_path = os.path.join(DOWNLOAD_DIR, title)

        # Tenta diferentes extensões e variações de nome
        possible_files = [
            f"{base_path}.mp3",
            f"{base_path}.m4a",
            os.path.join(DOWNLOAD_DIR, f"{title}.mp3"),
        ]

        # Procura qualquer .mp3 recém-criado no diretório
        import glob
        import time
        recent_mp3s = glob.glob(os.path.join(DOWNLOAD_DIR, "*.mp3"))
        if recent_mp3s:
            # Pega o mais recente
            filename = max(recent_mp3s, key=os.path.getctime)
            print(f"[DEBUG] Arquivo encontrado: {filename}")
            return filename, title, upload_date

        # Se não encontrou por glob, tenta os caminhos fixos
        for test_path in possible_files:
            if os.path.exists(test_path):
                print(f"[DEBUG] Arquivo encontrado: {test_path}")
                return test_path, title, upload_date

        raise FileNotFoundError(f"MP3 não encontrado. Tentei: {possible_files}")

def transcribe_audio(audio_path, model_name="base"):
    model = whisper.load_model(model_name)
    result = model.transcribe(audio_path)
    return result

def save_text(text, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(text)

def main():
    parser = argparse.ArgumentParser(description='Convert YouTube audio to text')
    parser.add_argument('url', type=str, help='YouTube video URL')
    args = parser.parse_args()

    print("Downloading audio...")
    audio_path, video_title, upload_date = download_audio(args.url)

    print("Transcribing audio...")
    result = transcribe_audio(audio_path, "base")

    print("Saving results...")
    base_name = f"{upload_date} - {video_title}.txt"
    final_path = os.path.join(DOWNLOAD_DIR, base_name)
    save_text(result["text"], final_path)

    print(f"Transcription saved to {final_path}")

if __name__ == "__main__":
    main()
