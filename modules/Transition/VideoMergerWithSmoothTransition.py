from PIL import Image, ImageFilter
import random
import os
from pathlib import Path
import cv2
import numpy as np

class VideoMergerWithSmoothTransition:
    def __init__(self, fps: int = 30, transition_duration: float = 0.5):
        self.fps = fps
        self.transition_duration = transition_duration

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

        transition_frames_count = int(self.fps * self.transition_duration)

        for i, video in enumerate(videos):
            ret, prev_frame = video.read()

            while ret:
                if i < len(videos) - 1 and not video.get(cv2.CAP_PROP_POS_FRAMES) < video.get(cv2.CAP_PROP_FRAME_COUNT) - transition_frames_count:
                    alpha = (video.get(cv2.CAP_PROP_POS_FRAMES) - (video.get(cv2.CAP_PROP_FRAME_COUNT) - transition_frames_count)) / transition_frames_count
                    ret_next, next_frame = videos[i + 1].read()
                    
                    if ret_next:
                        blended_frame = cv2.addWeighted(prev_frame, 1 - alpha, next_frame, alpha, 0)
                        out.write(blended_frame)
                        ret, prev_frame = video.read()
                        continue

                out.write(prev_frame)
                ret, prev_frame = video.read()

            video.release()

        out.release()

        print(f"Concatenated video saved to {output_filename}.")

if __name__ == '__main__':   
    # 使用例 (コメントアウトされています)
    merger = VideoMergerWithSmoothTransition()
    input_folder_path = r"image\Echoes-of-Creation_Blurred_mov"
    output_folder_path = f"{input_folder_path}_Final"
    os.makedirs(output_folder_path, exist_ok=True)
    output_video_path = os.path.join(output_folder_path, "concatenated_video.mp4")
    merger.merge_videos(input_folder_path, output_video_path)