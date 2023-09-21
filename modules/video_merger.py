from PIL import Image, ImageFilter
import random
import os
from pathlib import Path
import cv2
import numpy as np

from modules.Transition.VideoMergerWithSmoothTransition import VideoMergerWithSmoothTransition

if __name__ == '__main__':   
    # 使用例 (コメントアウトされています)
    merger = VideoMergerWithSmoothTransition()
    input_folder_path = r"image\Echoes-of-Creation_Blurred_mov"
    output_folder_path = f"{input_folder_path}_Final"
    os.makedirs(output_folder_path, exist_ok=True)
    output_video_path = os.path.join(output_folder_path, "concatenated_video.mp4")
    merger.merge_videos(input_folder_path, output_video_path)
