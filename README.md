# NIDAQ Voltammetry

NIDAQmx を使用して、ボルタンメトリーの波形を出力するプログラム

- main.py: メインの処理（これを実行する）
- daq.py: DAQ とのやりとりを行うモジュール
- waveform.py: ボルタンメトリーの波形を生成するための関数群

## 使い方

### 方法 A: 仮想環境を使わない

1. Python を実行できる環境を用意
1. コマンドプロンプトやターミナルで、このプログラムがあるディレクトリに移動
1. 下記を実行して、必要なモジュール（`requirements.txt`に記載）をインストール
   ```shell
   pip install -r requirements.txt
   ```
1. main.py を実行する
   ```shell
   python main.py
   ```
1. 必要に応じて、main.py の中身を変えてください
