from PIL import Image, ImageFilter
import random
import os
from pathlib import Path
import cv2
import numpy as np
from modules.utils import v_image_blurred_utils

class BlurredBackgroundEmbedder:
    def __init__(self, input_folder: str, height: int = 2000):
        """
        ImageProcessor クラスの初期化関数
        
        引数:
        - input_folder: 画像が保存されているフォルダのパス
        - height: 出力画像の希望の高さ（デフォルトは2000ピクセル）
        """
        self.input_folder = input_folder
        self.height = height
        self.output_folder = input_folder + "_Blurred"
        
        # 出力フォルダを作成
        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)

    def process_all_images(self):
        """
        指定されたフォルダ内のすべての画像を処理します。
        """
        image_files = [f for f in os.listdir(self.input_folder) if os.path.isfile(os.path.join(self.input_folder, f))]
        
        for image_file in image_files:
            input_image_path = os.path.join(self.input_folder, image_file)
            output_image_path = os.path.join(self.output_folder, image_file)
            v_image_blurred_utils.embed_image_on_blurred_background(input_image_path, output_image_path)

if __name__ == '__main__':
    # クラスの使用例
    processor = BlurredBackgroundEmbedder(r"image\Echoes-of-Creation")
    processor.process_all_images()