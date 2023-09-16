from PIL import Image, ImageFilter
import random
import os
from pathlib import Path
import cv2
import numpy as np
from modules.utils import v_image_blurred_utils
from modules.BlurredBackgroundEmbedder import BlurredBackgroundEmbedder
from modules.FrameVideoCreator import FrameVideoCreator
from modules.Transition.VideoMergerWithSmoothTransition import VideoMergerWithSmoothTransition


class VideoProcessingPipeline:
    def __init__(self, image_folder: str):
        """
        VideoProcessingPipeline クラスの初期化関数
        
        引数:
        - image_folder: 画像が格納されているフォルダのパス
        """
        self.image_folder = image_folder
        self.blurred_folder = f"{image_folder}_Blurred"
        self.video_folder = f"{self.blurred_folder}_mov"
        self.final_folder = f"{self.video_folder}_Final"
    
    def process_images(self):
        """
        画像のブラー処理を実行
        """
        processor = BlurredBackgroundEmbedder(self.image_folder)
        processor.process_all_images()

    def create_videos_from_images(self):
        """
        ブラー処理された画像から動画を作成
        """
        video_creator = FrameVideoCreator()
        video_creator.process_folder(self.blurred_folder)

    def merge_videos(self):
        """
        生成された動画を連結
        """
        os.makedirs(self.final_folder, exist_ok=True)
        output_video_path = os.path.join(self.final_folder, "concatenated_video.mp4")
        merger = VideoMergerWithSmoothTransition()
        merger.merge_videos(self.video_folder, output_video_path)

    def execute_pipeline(self):
        """
        画像の処理、動画の作成、動画の連結を順番に実行
        """
        self.process_images()
        self.create_videos_from_images()
        self.merge_videos()
        print("Video processing completed!")

if __name__ == '__main__':
    pipeline = VideoProcessingPipeline(r"image\The-Multifaceted-Dawn")
    pipeline.execute_pipeline()