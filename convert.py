import os
import sys
import time
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import ffmpeg

def convert_to_mov(input_path, output_path):
    ffmpeg.input(input_path).output(output_path, vcodec="libx264", acodec="pcm_s16le").run(overwrite_output=True)


class VideoConversionHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return

        input_file = event.src_path
        if input_file.lower().endswith((".mp4", ".mkv")):
            output_file = os.path.splitext(input_file)[0] + ".mov"
            convert_to_mov(input_file, output_file)
            print(f"Converted: {input_file} -> {output_file}")

def convert_existing_files(folder_path):
    for input_file in folder_path.glob("*"):
        if input_file.is_file() and input_file.suffix.lower() in {".mp4", ".mkv"}:
            output_file = input_file.with_suffix(".mov")
            convert_to_mov(str(input_file), str(output_file))
            print(f"Converted: {input_file} -> {output_file}")

def watch_folder(folder_path):
    event_handler = VideoConversionHandler()
    observer = Observer()
    observer.schedule(event_handler, folder_path, recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    folder_path = "/home/hhgsx/Videos/ConvertedMov"
    folder_path = Path(folder_path).resolve()

    if not folder_path.is_dir():
        print(f"Error: {folder_path} is not a valid directory.")
        sys.exit(1)

    print(f"Converting existing files in folder: {folder_path}")
    convert_existing_files(folder_path)

    print(f"Watching folder: {folder_path}")
    watch_folder(folder_path)
