# NIDAQ Voltammetry

NIDAQmx を使用して、ボルタンメトリーの波形を出力するプログラム

- main.py: メインの処理（これを実行する）
- daq.py: DAQ とのやりとりを行うモジュール
- waveform.py: ボルタンメトリーの波形を生成するための関数群

## 使い方

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

## 出力例

### Cyclic Square Wave (CSW)

```python
# 波形のパラメータ
sample_rate=100000  # サンプリング周波数
E_SW = 0.4          # 矩形波の振幅
E_initial = -0.1    # 初期電圧
E_holding = 0.2     # 待機電圧（gapの電圧）
E_peak1 = 1.3       # 第１ピークの電圧 (switching potential?)
E_peak2 = -1.3      # 第２ピークの電圧
E_staircase = 12.5e-3 # 矩形波の周期ごとに上昇/下降させる電圧幅 (12.5 to 75 mV)
tau = 1e-3          # 二相性矩形波の１周期の時間
gap = 2e-3          # 待機の時間 (0 to 4 ms)
num_csw = 7         # cycleの数
```

#### 全体

<img src="/example/csw_full.png" alt="CSW全体" />

#### 最初の立ち上がり

<img src="/example/csw_1st_rise.png" alt="CSW最初の立ち上がり" />

#### 最初の立ち下がり

<img src="/example/csw_1st_fall.png" alt="CSW最初の立ち下がり" />

#### 最初の gap

<img src="/example/csw_1st_gap.png" alt="CSW最初のgap" />
