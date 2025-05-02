"""
# Main - NIDAQmx Voltammetry

NIDAQmxを使用して、ボルタンメトリーの波形を出力する。

吉川隆洋
"""
# モジュールのインポート -----

# pip install が必要なモジュール
import numpy as np
import matplotlib.pyplot as plt

# 自作モジュール
import waveform as wf
import daq


# パラメーターの設定 -----

# 波形のパラメータ
sample_rate=100000  # サンプリング周波数
E_SW = 0.4          # 矩形波の振幅
E_initial = -0.1    # 初期電圧
E_holding = 0.2     # 待機電圧（gapの電圧）
E_peak1 = 1.3       # 第１ピークの電圧 (switching potential?)
# E_peak2 = -0.5875    # 第２ピークの電圧
E_peak2 = -1.3    # 第２ピークの電圧
E_staircase = 12.5e-3 # 矩形波の周期ごとに上昇/下降させる電圧幅 (12.5 to 75 mV)
tau = 1e-3          # 二相性矩形波の１周期の時間
gap = 2e-3          # 待機の時間 (0 to 4 ms)
num_csw = 7         # cycleの数

# DAQのパラメータ
OUTPUT = True # 出力するかどうか 
device_name = "Dev1" # DAQデバイス名
ao_channel = "ao0"   # 出力チャネル名
chunk_size = None    # チャンクサイズ（Noneの場合は全てのデータを一度に出力）


# プロットのパラメータ
PLOT = True # プロットを表示するかどうか
figure_kwargs = {
    "figsize": (6, 4), # (width, height) inch
    "dpi": 200,
    "tight_layout": True,
}
plot_kwargs = {
    "color": "black",
    "linestyle": "-",
    "linewidth": 0.5,
}
grid_kwargs = {
    "color": "gray",
    "linestyle": "-",
    "linewidth": 0.2,
}
xlabel_kwargs = {"xlabel": "Time (s)"} 
ylabel_kwargs = {"ylabel": "Potential (V)"}

def main():
    # Cyclic Square Wave (CSW) の波形を生成 -----

    csw = wf.get_cyc_square_wave(
        sample_rate=sample_rate,
        E_SW=E_SW,
        E_initial=E_initial,
        E_holding=E_holding,
        E_peak1=E_peak1,
        E_peak2=E_peak2,
        E_staircase=E_staircase,
        tau=tau,
        gap=gap,
        num_csw=num_csw
    )


    # プロット -----
    if PLOT:
        time = np.arange(csw.shape[0]) / sample_rate

        plt.figure(**figure_kwargs)
        plt.grid(**grid_kwargs)
        plt.plot(time, csw, **plot_kwargs)
        plt.xlabel(**xlabel_kwargs)
        plt.ylabel(**ylabel_kwargs)

        plt.show()
    
    # DAQで出力 -----
    if OUTPUT:
        # DAQが接続されているか確認
        if daq.device_connected():
            print("DAQの接続を確認しました")

            # 波形を出力
            # daq.play(csw, sample_rate, device_name, ao_channel, chunk_size)
        else:
            print("DAQが接続されていません")

if __name__ == "__main__":
    main()