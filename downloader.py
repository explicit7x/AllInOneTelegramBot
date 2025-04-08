from pyrogram import Client, filters
from pyrogram.types import Message
import yt_dlp
import os

def download_video(url: str, user_id: int):
    output_path = f"downloads/{user_id}.mp4"
    ydl_opts = {
        'format': 'best[ext=mp4]',
        'outtmpl': output_path,
        'quiet': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            ydl.download([url])
            return output_path
        except Exception as e:
            print(f"Download Error: {e}")
            return None

def is_valid_url(url: str):
    return url.startswith("http://") or url.startswith("https://")
