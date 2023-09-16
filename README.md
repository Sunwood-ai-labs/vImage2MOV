
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

## 画像のブラー処理

このツールは、画像にブラー背景を追加して、元の画像をその上に配置することで、魅力的なビジュアルエフェクトを追加します。具体的には、画像が9:16のアスペクト比で中央に配置され、背景はその画像のブラーしたバージョンです。

### ステップ1: 必要なライブラリのインポート 
- `PIL` (Pillow): 画像の読み込み、加工、保存を行うためのライブラリ。 
- `random`, `os`, `pathlib`: ファイル操作やランダムな数値の生成に使用。 
- `cv2` (OpenCV): 画像や動画の処理を行うためのライブラリ。 
- `numpy`: 数値計算を行うためのライブラリ。 
- `modules.utils`: 他のカスタムモジュールからの関数のインポート。

### ステップ2: `BlurredBackgroundEmbedder` クラスの解説

```python

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
```

このクラスは、指定されたフォルダ内のすべての画像にブラー効果を適用し、結果を新しいフォルダに保存します。

#### コンストラクタ: 
- `input_folder`: ブラー効果を適用する画像が保存されているフォルダのパス。 
- `height`: 出力画像の高さ（デフォルトは2000ピクセル）。 
- `output_folder`: 出力された画像が保存されるフォルダ。入力フォルダの名前に "_Blurred" を追加したものになります。

#### `process_all_images` メソッド:

このメソッドは、指定されたフォルダ内のすべての画像を処理し、ブラー背景を適用した画像を新しいフォルダに保存します。


### ステップ3: `embed_image_on_blurred_background` 関数の解説

```python

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
```
この関数は、指定された画像にブラー背景を追加し、結果を指定されたパスに保存します。
#### 主なステップ:
1. 画像を読み込む。
2. 画像の元のサイズを取得する。
3. 9:16のアスペクト比での出力画像の幅を計算する。
4. 元の画像をブラーする。
5. ブラーした画像を指定された高さと計算された幅にリサイズする。
6. 元の画像を指定された高さにリサイズし、アスペクト比を維持する。
7. リサイズされた元の画像をブラーした背景の中央に配置する。
8. 画像を指定されたパスに保存する。

## 動画の作成

このツールは、指定されたフォルダ内の画像を使用して動画を生成します。動画は、画像を上から下にスクロールするエフェクトを持っています。各動画は、昇順と降順のエフェクトを交互に適用します。

### ステップ1: 必要なライブラリとモジュールのインポート 
- `PIL` (Pillow): 画像の読み込み、加工、保存を行うためのライブラリ。 
- `random`, `os`, `pathlib`: ファイル操作やランダムな数値の生成に使用。 
- `cv2` (OpenCV): 画像や動画の処理を行うためのライブラリ。 
- `numpy`: 数値計算を行うためのライブラリ。 
- `modules.utils.image_frame_generator`: 他のカスタムモジュールからの関数のインポート。

### ステップ2: `FrameVideoCreator` クラスの解説

```python

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
```

このクラスは、指定されたフォルダ内のすべての画像を取得し、それらの画像を使用して動画を生成します。

#### コンストラクタ: 
- `fps`: 動画のフレームレート。デフォルトは30FPSです。 
- `ascending_order`: フレームの順番を制御するフラグ。デフォルトはTrue（昇順）です。

#### `create_video_from_frames` メソッド:


このメソッドは、与えられた画像フレームのリストを使用して動画を作成します。動画は、昇順と降順のエフェクトを交互に適用します。

#### `process_folder` メソッド:

このメソッドは、指定されたフォルダ内のすべての画像を処理し、それぞれの画像を使用して動画を生成します。
### ステップ3: `generate_centered_moving_frames` 関数の解説

```python

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
```

この関数は、指定された画像を上から下にスクロールさせるエフェクトで動画を生成します。クロップは、画像の中心を基準に行われます。

#### 主なステップ:

1. 画像を読み込む。
2. アスペクト比を維持したまま、指定の幅にリサイズ。
3. ランダムな倍率で画像を拡大。
4. 画像を上から下にスクロールさせるエフェクトでクロップしたフレームを生成。


## 動画の連結

このツールは、指定されたフォルダ内の動画を取得し、それらを連結して1つの動画を作成します。動画間の遷移にはアルファブレンドが使用され、スムーズな遷移が行われます。このチュートリアルでは、このツールの使用方法と内部の動作をステップバイステップで解説します。

### ステップ1: 必要なライブラリとモジュールのインポート 
- `PIL`: 画像の読み込み、加工、保存を行うためのライブラリ。 
- `random`, `os`, `pathlib`: ファイル操作やランダムな数値の生成に使用。 
- `cv2` (OpenCV): 画像や動画の処理を行うためのライブラリ。 
- `numpy`: 数値計算を行うためのライブラリ。

### ステップ2: `VideoMergerWithSmoothTransition` クラスの解説

```python

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
    merger = VideoMergerWithSmoothTransition()
    input_folder_path = r"image\Echoes-of-Creation_Blurred_mov"
    output_folder_path = f"{input_folder_path}_Final"
    os.makedirs(output_folder_path, exist_ok=True)
    output_video_path = os.path.join(output_folder_path, "concatenated_video.mp4")
    merger.merge_videos(input_folder_path, output_video_path)
```

このクラスは、指定されたフォルダ内のすべての動画を取得し、それらを連結して1つの動画を作成します。

#### コンストラクタ: 
- `fps`: 生成される動画のフレームレート。デフォルトは30FPSです。 
- `transition_duration`: 動画間の遷移の期間。デフォルトは0.5秒です。

#### `merge_videos` メソッド:

このメソッドは、指定されたフォルダ内のすべての動画を連結します。動画間の遷移は、アルファブレンドを使用してスムーズに行われます。
1. 指定されたフォルダ内の動画ファイルのリストを取得します。 
2. 各動画の最後の数フレームと次の動画の最初の数フレームをブレンドします。このブレンドの期間は、`transition_duration`で指定されます。
3. ブレンディングが完了したら、結果の動画を指定されたファイルパスに保存します。

### ステップ3: メインの実行部分

この部分は、上記で定義したクラスを実際に使用して動画を連結するためのコードです。指定された入力フォルダから動画を取得し、それらを連結して出力フォルダに保存します。


## 統合パイプライン

このツールは、指定されたフォルダ内の画像を取得し、それらの画像から動画を生成し、それらを1つの動画に連結します。このチュートリアルでは、このツールの使用方法と内部の動作をステップバイステップで解説します。

### ステップ1: 必要なライブラリとモジュールのインポート 
- `PIL`: 画像の読み込み、加工、保存を行うためのライブラリ。 
- `random`, `os`, `pathlib`: ファイル操作やランダムな数値の生成に使用。 
- `cv2` (OpenCV): 画像や動画の処理を行うためのライブラリ。 
- `numpy`: 数値計算を行うためのライブラリ。
- 各種モジュール: このツールの核心部分となる処理を担当するカスタムモジュール。

### ステップ2: `VideoProcessingPipeline` クラスの解説

```python

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
```

このクラスは、画像のブラー処理、動画の作成、動画の連結という一連の処理を実行するためのパイプラインを提供します。

#### コンストラクタ: 
- `image_folder`: 画像が格納されているフォルダのパスを受け取り、それを基に各種処理のためのフォルダのパスを設定します。
#### `process_images` メソッド:

このメソッドは、指定されたフォルダ内のすべての画像にブラー処理を適用します。
#### `create_videos_from_images` メソッド:

このメソッドは、ブラー処理された画像を使用して動画を生成します。
#### `merge_videos` メソッド:

このメソッドは、生成されたすべての動画を1つの動画に連結します。
#### `execute_pipeline` メソッド:

画像のブラー処理、動画の生成、動画の連結という一連の処理を順に実行します。
### ステップ3: メインの実行部分

この部分は、上記で定義したクラスを実際に使用して一連の処理を実行するコードです。指定されたフォルダの画像を使用して、最終的に1つの動画を生成します。

## 最終的な動画

上記のコードで生成された動画に音楽とタイトルを入れれば簡単に下記のような動画になります。



## まとめ

Pythonを使用して、手持ちの画像からSNSに投稿するための動画を簡単に自動生成する方法を学びました。この方法を活用すれば、視覚的に魅力的なSNSの投稿を簡単に作成できます。初心者の方でも、ステップを追って実行すれば、手軽に動画を生成できるので、ぜひ試してみてください。
