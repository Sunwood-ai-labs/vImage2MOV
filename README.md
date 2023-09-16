
# VideoProcessingPipeline(SNS投稿動画生成ツール)

SNSの投稿は、画像よりも動画の方が注目を集めやすいことが多いです。しかし、動画を作成するのは手間がかかるもの。そこで、手持ちの画像から自動で魅力的な動画を生成する方法をご紹介します。

![](https://hamaruki.com/wp-content/uploads/2023/09/00028-1365031933-1-576x1024.png)


## 概要

### ステップ1: 必要なツールの準備
- Python環境
- OpenCV
- PIL (Pillow)

これらはpipを使って簡単にインストールできます。

```bash

pip install opencv-python pillow
```


### ステップ2: 画像の準備

まず、動画に変換したい画像を一つのフォルダにまとめます。このフォルダのパスを後で使用します。
### ステップ3: 画像のブラー処理

動画を作成する前に、画像にブラー効果を適用します。これにより、動画が洗練された雰囲気を持つようになります。

以下のクラス、`BlurredBackgroundEmbedder`を使用して、画像にブラー効果を適用します。

```python

processor = BlurredBackgroundEmbedder(r"path/to/your/image_folder")
processor.process_all_images()
```


### ステップ4: 動画の作成

ブラー処理された画像を使用して、動画を作成します。この動画は、画像が上から下にスクロールするアニメーションを持っています。

以下のクラス、`FrameVideoCreator`を使用して動画を作成します。

```python

video_creator = FrameVideoCreator()
video_creator.process_folder(r"path/to/your/image_folder_Blurred")
```


### ステップ5: 動画の連結

複数の動画を一つに連結します。また、動画間の遷移はスムーズなアルファブレンドが適用されます。

```python

merger = VideoMergerWithSmoothTransition()
input_folder_path = r"path/to/your/image_folder_Blurred_mov"
output_folder_path = f"{input_folder_path}_Final"
os.makedirs(output_folder_path, exist_ok=True)
output_video_path = os.path.join(output_folder_path, "concatenated_video.mp4")
merger.merge_videos(input_folder_path, output_video_path)
```


### ステップ6: 動画の確認

出力フォルダに保存された動画を確認します。この動画をSNSにアップロードすることで、魅力的な投稿を簡単に作成できます。


## 使用方法

`VideoProcessingPipeline`は、指定された画像フォルダ内の画像を処理し、動画を作成し、動画を連結する一連のタスクを実行するPythonクラスです。

### クイックスタート

1. まず、必要なモジュールをインポートします。

```python

from modules.utils import v_image_blurred_utils
from modules.BlurredBackgroundEmbedder import BlurredBackgroundEmbedder
from modules.FrameVideoCreator import FrameVideoCreator
from modules.Transition.VideoMergerWithSmoothTransition import VideoMergerWithSmoothTransition
```

 
1. `VideoProcessingPipeline`クラスを初期化します。このとき、画像が格納されているフォルダのパスを引数として渡します。

```python

pipeline = VideoProcessingPipeline(r"path/to/your/image_folder")
```

 
1. `execute_pipeline`メソッドを呼び出して、画像の処理、動画の作成、動画の連結を順番に実行します。

```python

pipeline.execute_pipeline()
```


### 内部の動作 
- **画像のブラー処理** : 画像にブラー効果を適用し、新しいフォルダに保存します。 
- **動画の作成** : ブラー処理された画像から、上から下に移動するアニメーション効果を持つ動画を作成します。 
- **動画の連結** : すべての動画を一つの動画に連結します。動画間の遷移はスムーズなアルファブレンドが適用されます。

### 注意点
- 入力として渡される画像フォルダには、連結したい画像のみが含まれていることを確認してください。 
- 生成される動画は、`image_folder_Blurred_mov_Final`という名前のフォルダに保存されます。


## 解説サイト

詳細な解説はこちら

https://hamaruki.com/automatically-generate-posted-videos-from-images/

## まとめ

Pythonを使用して、手持ちの画像からSNSに投稿するための動画を簡単に自動生成する方法を学びました。この方法を活用すれば、視覚的に魅力的なSNSの投稿を簡単に作成できます。初心者の方でも、ステップを追って実行すれば、手軽に動画を生成できるので、ぜひ試してみてください。
