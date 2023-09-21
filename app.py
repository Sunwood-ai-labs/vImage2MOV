import os
import gradio as gr
from main import VideoProcessingPipeline
import shutil
from art import *
from loguru import logger

def remove_temp_folder():
    logger.info("remove ...")
    """一時的なフォルダを削除する関数"""
    temp_dir = "_tmp"
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)

def process_uploaded_images(files):
    logger.info("uploaded ...")
    # _tmpフォルダ内に一時的なフォルダを作成して、アップロードされた画像を保存
    remove_temp_folder()  # 起動時に一時的なフォルダを削除
    temp_folder = "_tmp/temp_uploaded_images"
    os.makedirs(temp_folder, exist_ok=True)
    
    for file in files:
        # 新しい保存先のパスを生成
        new_path = os.path.join(temp_folder, os.path.basename(file.name))
        # ファイルを新しい場所にコピー
        shutil.copy(file.name, new_path)
    
    # VideoProcessingPipelineを実行
    logger.info("Processing ...")
    pipeline = VideoProcessingPipeline(temp_folder)
    pipeline.execute_pipeline()
    
    logger.info(".... Fin")
    # 最終的に生成された動画のパスを返す
    return os.path.join(pipeline.final_folder, "concatenated_video.mp4")

demo = gr.Interface(
    process_uploaded_images,
    gr.File(file_count=5, file_types=[".jpg", ".jpeg", ".png"]),
    gr.Video(),
    title="Image to Video Processing"
)

if __name__ == "__main__":
    tprint("Image to Video Processing")

    
    demo.launch()