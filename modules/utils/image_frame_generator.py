from PIL import Image, ImageFilter
import random
import os
from pathlib import Path
import cv2
import numpy as np

def generate_centered_moving_frames(input_path: str, crop_width: int = 1620, crop_height: int = 2880, min_frames_required: int = 120):
    """
    画像を上から下に移動させて、指定されたサイズでクロップしたフレームを生成します。
    クロップは画像の中心を基準に行います。
    
    引数:
    - input_path: 入力画像のパス
    - crop_width: クロップする幅
    - crop_height: クロップする高さ
    
    戻り値:
    - クロップされたフレームのリスト
    """
    
    image = Image.open(input_path)
    aspect_ratio = image.height / image.width
    new_height_initial_resize = int(crop_width * aspect_ratio)
    resized_initial = image.resize((crop_width, new_height_initial_resize))
    
    resize_factor = random.uniform(1.2, 1.5)
    new_width = int(resized_initial.width * resize_factor)
    new_height = int(resized_initial.height * resize_factor)
    resized_image = resized_initial.resize((new_width, new_height))
    
    frames = []
    max_y_offset = max(new_height - crop_height, 0)
    
    # クロップの中心を維持するためのx_offsetを計算
    x_offset = (new_width - crop_width) // 2
    
    step = max_y_offset // min_frames_required
    for y_offset in range(0, max_y_offset + 1, step):
        frame = resized_image.crop((x_offset, y_offset, x_offset + crop_width, y_offset + crop_height))
        frames.append(frame)
    
    return frames

if __name__ == '__main__':    
    # フレームを生成する
    frames_modified = generate_centered_moving_frames(r"image\Echoes-of-Creation_Blurred\00028-1365031933.png")

    print(len(frames_modified))