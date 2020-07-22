# PBL_eshiritori
## 環境構築
pbl.ymlを用いてAnaconda上で環境構築を行うことができます。
```
conda env create -n env_name -f pbl.yml
```
env_nameのところに環境につけたい名前を入れます。指定しない場合は自動的にpblになります。
上のコマンドを入力しpyaudio辺りでエラーになる場合は
```
sudo apt-get install portaudio19-dev
```
でportaudioをインストールすると直る場合があります。
## 各ファイルの説明
### voice_input.py
マイクからの音声をひらがなの文字列に変換します。無音やひらがなに変換できない単語は棄却して、再び録音を開始します。
### one_stroke_path.py
pngなどの画像ファイルを読み込み、画像を一筆書きできる関数を出力します。
#### Uses
1. img2functionフォルダ内に変換したい画像ファイルを置きます
1. one_stroke.py "file_name"
