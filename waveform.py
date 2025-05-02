"""
# Waveform - NIDAQmx Voltammetry

ボルタンメトリーの波形を生成するための関数群

吉川隆洋
"""


import numpy as np

def get_square_wave(
    sample_rate: int,
    duration: float,
    amplitude: float,
    bias: float = 0
):
    """矩形波を生成"""
    n_samples = round(sample_rate * duration)
    sw = np.ones(n_samples) * bias

    sw[:n_samples // 2] = bias + amplitude
    sw[n_samples // 2:] = bias - amplitude

    return sw

def get_cyc_square_wave_1cycle(
    sample_rate: int,   # サンプリング周波数
    E_SW: float,        # 矩形波の振幅
    E_initial: float,   # 初期電圧
    E_holding: float,   # 待機電圧（gapの電圧）
    E_peak1: float,     # 第１ピークの電圧 (switching potential?)
    E_peak2: float,     # 第２ピークの電圧 (switching potential?)
    E_staircase: float, # 矩形波の周期ごとに上昇/下降させる電圧幅 
    tau: float,         # 二相性矩形波の１周期の時間
):
    """1サイクル分のCSW (Cyclic Square Wave) の波形を生成"""

    # 最初の矩形波 ---
    csw_1cycle = []
    bias = E_initial
    csw_1cycle += list(get_square_wave(
        sample_rate=sample_rate,
        duration=tau,
        amplitude=E_SW,
        bias=bias
    ))

    # 正ピークまでの波形 ---

    # 割り切れるかチェック
    dE = (E_peak1 - E_SW) - E_initial
    n_sw_peak1 = round(dE / E_staircase, 9)
    if n_sw_peak1.is_integer() == False:
        raise ValueError("(E_peak1 - E_SW) - E_initial を E_staircase で割り切れません")

    # 整数に変換
    n_sw_peak1 = round(n_sw_peak1)

    # 矩形波の振幅を上昇させながら生成
    for i in range(n_sw_peak1):
        bias += E_staircase
        sw = get_square_wave(
            sample_rate=sample_rate,
            duration=tau,
            amplitude=E_SW,
            bias=bias
        )
        csw_1cycle += list(sw)


    # 負ピークまでの波形 ---

    # 割り切れるかチェック
    dE = (E_peak1 - 2 * E_SW) - E_peak2
    n_sw_peak2 = round(dE / E_staircase, 9)
    if n_sw_peak2.is_integer() == False:
        raise ValueError("(E_peak1 - 2 * E_SW) - E_peak2 を E_staircase で割り切れません")

    # 整数に変換
    n_sw_peak2 = round(n_sw_peak2)

    # 矩形波の振幅を下降させながら生成
    for i in range(n_sw_peak2):
        bias -= E_staircase
        sw = get_square_wave(
            sample_rate=sample_rate,
            duration=tau,
            amplitude=E_SW,
            bias=bias
        )
        csw_1cycle += list(sw)

    # gapまでの波形 ---
    
    # 上昇できるかチェック
    dE = E_holding - (E_peak2 + 2 * E_SW)
    if dE < 0:
        raise ValueError("E_holding - (E_peak2 + 2 * E_SW) が負の値です")

    # 割り切れるかチェック
    n_sw_gap = round(dE / E_staircase, 9)
    if n_sw_gap.is_integer() == False:
        raise ValueError("(E_holding - (E_peak2 + 2 * E_SW)) を E_staircase で割り切れません")

    # 整数に変換
    n_sw_gap = round(n_sw_gap)

    # 矩形波の振幅を上昇させながら生成
    for i in range(n_sw_gap):
        bias += E_staircase
        sw = get_square_wave(
            sample_rate=sample_rate,
            duration=tau,
            amplitude=E_SW,
            bias=bias
        )
        csw_1cycle += list(sw)

    csw_1cycle = np.array(csw_1cycle)

    return csw_1cycle

def get_cyc_square_wave(
    sample_rate: int,   # サンプリング周波数
    E_SW: float,        # 矩形波の振幅
    E_initial: float,   # 初期電圧
    E_holding: float,   # 待機電圧（gapの電圧）
    E_peak1: float,     # 第１ピークの電圧 (switching potential?)
    E_peak2: float,     # 第２ピークの電圧 (switching potential?)
    E_staircase: float, # 矩形波の周期ごとに上昇/下降させる電圧幅 
    tau: float,         # 二相性矩形波の１周期の時間
    gap: float,         # 待機の時間
    num_csw: int,       # cycleの数
):
    """CSW (Cyclic Square Wave) の波形を生成"""

    csw = []
    for i in range(num_csw):
        csw_1cycle = get_cyc_square_wave_1cycle(
            sample_rate=sample_rate,
            E_SW=E_SW,
            E_initial=E_initial,
            E_holding=E_holding,
            E_peak1=E_peak1,
            E_peak2=E_peak2,
            E_staircase=E_staircase,
            tau=tau
        )
        csw += list(csw_1cycle)

        # 最後のループはgapを追加しない
        if i == num_csw - 1:
            break

        # gapの時間を追加
        sw = get_square_wave(
            sample_rate=sample_rate,
            duration=gap,
            amplitude=0,
            bias=E_holding
        )
        csw += list(sw)
    
    return np.array(csw)

