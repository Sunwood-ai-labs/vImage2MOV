from PIL import Image, ImageFilter
import random
import os
from pathlib import Path
import cv2
import numpy as np

def embed_image_on_blurred_background(input_path: str, output_path: str, height: int = 2000) -> None:
    """
    入力画像をブラーしたバージョンの上に配置し、その結果を保存します。
    
    引数:
    - input_path: 入力画像のパス
    - output_path: 処理された画像を保存する場所
    - height: 出力画像の希望の高さ（デフォルトは2000ピクセル）
    """
    
    # 与えられたパスから画像を読み込む
    image = Image.open(input_path)
    
    # 画像の元のサイズを取得する
    original_width, original_height = image.size
    
    # 9:16のアスペクト比と指定された高さに基づいて、出力画像の幅を計算する
    target_width = int(height * 9 / 16)
    
    # 元の画像のブラーしたバージョンを作成する
    blurred_image = image.filter(ImageFilter.GaussianBlur(20))
    
    # ブラー画像を希望の出力サイズにリサイズする
    resized_blurred_background = blurred_image.resize((target_width, height))
    
    # 元のアスペクト比を保持したまま、元の画像を指定された高さにリサイズする
    new_width = int(original_width * (height / original_height))
    resized_image_keep_aspect = image.resize((new_width, height), Image.ANTIALIAS)
    
    # リサイズされた元の画像をブラーした背景の中央に配置する位置を計算する
    x_offset = (resized_blurred_background.width - resized_image_keep_aspect.width) // 2
    y_offset = (resized_blurred_background.height - resized_image_keep_aspect.height) // 2
    
    # 画像に透明度がある場合（RGBAモード）、背景にペーストする際のマスクとして使用する
    mask_keep_aspect = resized_image_keep_aspect if resized_image_keep_aspect.mode == "RGBA" else None
    
    # リサイズされた元の画像をブラーした背景の上にオーバーレイする
    resized_blurred_background.paste(resized_image_keep_aspect, (x_offset, y_offset), mask_keep_aspect)
    
    # 指定されたパスに結合された画像を保存する
    resized_blurred_background.save(output_path)