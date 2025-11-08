#!/usr/bin/env python3

import sys
import os
import subprocess
import datetime

def get_venv_exec(bin_name, venv_path):
    """Retorna o path para o executável dentro do venv."""
    return os.path.join(venv_path, "bin", bin_name)

def download_reel_audio(url, output_path, yt_dlp_exec):
    print("[+] Baixando áudio do Reel...")
    command = [
        yt_dlp_exec,
        "-f", "bestaudio",
        "--extract-audio",
        "--audio-format", "mp3",
        "-o", f"{output_path}.%(ext)s",
        url
    ]
    subprocess.run(command, check=True)
    print("[+] Áudio baixado com sucesso.")

def transcribe_audio(audio_file, output_dir, whisper_exec):
    print("[+] Transcrevendo áudio...")
    command = [
        whisper_exec,
        audio_file,
        "--model", "small",
        "--language", "pt",
        "--task", "transcribe",
        "--output_format", "txt",
        "--output_dir", output_dir
    ]
    subprocess.run(command, check=True)
    print("[+] Transcrição concluída.")

def main():
    if len(sys.argv) != 2:
        print("Uso: ig-to-txt <URL_do_Reel>")
        sys.exit(1)

    url = sys.argv[1]
    now = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Pega diretório atual
    current_dir = os.getcwd()
    base_output_path = os.path.join(current_dir, now)

    venv_path = os.path.expanduser("~/Downloads/venv")
    yt_dlp_exec = get_venv_exec("yt-dlp", venv_path)
    whisper_exec = get_venv_exec("whisper", venv_path)

    # Verificação se os binários existem
    if not (os.path.exists(yt_dlp_exec) and os.path.exists(whisper_exec)):
        print("[-] yt-dlp ou whisper não encontrados dentro do venv.")
        sys.exit(1)

    try:
        download_reel_audio(url, base_output_path, yt_dlp_exec)

        audio_file = f"{base_output_path}.mp3"

        transcribe_audio(audio_file, current_dir, whisper_exec)

        txt_file = os.path.join(current_dir, f"{now}.txt")
        print(f"[+] Arquivo TXT salvo em: {txt_file}")

    except subprocess.CalledProcessError as e:
        print(f"Erro ao executar comando: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()