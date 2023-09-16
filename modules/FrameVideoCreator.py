from PIL import Image, ImageFilter
import random
import os
from pathlib import Path
import cv2
import numpy as np
from modules.utils import image_frame_generator

class FrameVideoCreator:
    def __init__(self, fps: int = 30):
        """
        FrameVideoCreator クラスの初期化関数
        
        引数:
        - fps: 動画のフレームレート (デフォルトは30FPS)
        """
        self.fps = fps

        # 昇順（上から下）のエフェクトを初めに適用
        self.ascending_order = True
    
    def create_video_from_frames(self, frames: list, output_path: str):
        """
        与えられた画像フレームのリストから動画を作成します。動画ごとに昇順と降順のエフェクトを交互に適用します。
        
        引数:
        - frames: 画像フレームのリスト
        - output_path: 保存する動画のパス
        """
        frames_bgr = [cv2.cvtColor(np.array(frame), cv2.COLOR_RGB2BGR) for frame in frames]
        
        # 昇順か降順のエフェクトを適用するかに基づいて、フレームの順番を変更
        if not self.ascending_order:
            frames_bgr = list(reversed(frames_bgr))
        
        # 次回の動画生成のためにエフェクトの順番を切り替え
        self.ascending_order = not self.ascending_order
        
        height, width, layers = frames_bgr[0].shape
        size = (width, height)
        out = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*'MP4V'), self.fps, size)
        
        for frame in frames_bgr:
            out.write(frame)
        
        out.release()

    def process_folder(self, input_folder: str):
        """
        指定したフォルダ内の画像を処理し、動画を生成します。
        
        引数:
        - input_folder: 画像が保存されているフォルダのパス
        """
        output_folder = f"{input_folder}_mov"
        Path(output_folder).mkdir(parents=True, exist_ok=True)

        for image_file in Path(input_folder).glob("*.png"):
            frames = image_frame_generator.generate_centered_moving_frames(str(image_file))
            output_video_path = Path(output_folder) / f"{image_file.stem}.mp4"
            self.create_video_from_frames(frames, str(output_video_path))

if __name__ == '__main__':   
    # クラスの使用例
    video_creator = FrameVideoCreator()
    video_creator.process_folder(r"image/Echoes-of-Creation_Blurred")