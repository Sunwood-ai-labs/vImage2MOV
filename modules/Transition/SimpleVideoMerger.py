from PIL import Image, ImageFilter
import random
import os
from pathlib import Path
import cv2
import numpy as np


class SimpleVideoMerger:
    def __init__(self, fps: int = 30):
        self.fps = fps

    def merge_videos(self, input_folder: str, output_filename: str):
        video_files = [f for f in Path(input_folder).glob("*.mp4")]

        if not video_files:
            print("No video files found in the specified directory.")
            return

        videos = []

        for video_file in video_files:
            video = cv2.VideoCapture(str(video_file))
            videos.append(video)

        width = int(videos[0].get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(videos[0].get(cv2.CAP_PROP_FRAME_HEIGHT))

        fourcc = cv2.VideoWriter_fourcc(*'MP4V')
        out = cv2.VideoWriter(output_filename, fourcc, self.fps, (width, height))

        for i, video in enumerate(videos):
            ret, frame = video.read()

            while ret:
                out.write(frame)
                ret, frame = video.read()

            video.release()

        out.release()

        print(f"Concatenated video saved to {output_filename}.")

if __name__ == '__main__':   
    # 使用例 (コメントアウトされています)
    merger = SimpleVideoMerger()
    input_folder_path = r"image\Echoes-of-Creation_Blurred_mov"
    output_folder_path = f"{input_folder_path}_Final"
    os.makedirs(output_folder_path, exist_ok=True)
    output_video_path = os.path.join(output_folder_path, "concatenated_video.mp4")
    merger.merge_videos(input_folder_path, output_video_path)