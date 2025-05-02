"""
# DAQ

DAQとのやりとりを行うモジュール
"""

import numpy as np
import nidaqmx
import nidaqmx.system
import nidaqmx.errors

def device_connected():
    """接続されているNI DAQデバイスを確認する関数"""
    try:
        system = nidaqmx.system.System.local()
        devices = system.devices

        return len(devices) > 0
    except nidaqmx.errors.DaqNotSupportedError:
        print("DAQmxはこのシステムに対応していません")
    except Exception as e:
        print(e)
        return False

def play(outwave: np.ndarray, fs: int, device_name: str, ao_channel: str, chunk_size: int | None = None):
    """DAQmxを使用して波形を出力する関数"""
    
    n_samples = len(outwave)
    wave_duration = n_samples / fs

    try:
        with nidaqmx.Task() as output_task:
            # チャンネルを登録
            output_task.ao_channels.add_ao_voltage_chan(f"{device_name}/{ao_channel}")

            # サンプリングレートを設定
            output_task.timing.cfg_samp_clk_timing(
                rate=fs,
                source="OnboardClock",
            )

            # 波形を出力
            wait_duration = wave_duration + 1
            if isinstance(chunk_size, int) and chunk_size > 0:
                # チャンクサイズを指定して出力
                for i in range(0, n_samples, chunk_size):
                    chunk = outwave[i:i + chunk_size]
                    output_task.write(chunk, auto_start=True)
            else:
                # 全てのデータを一度に出力（長いとバッファオーバーする可能性あり）
                output_task.write(outwave, auto_start=True)

            # 出力が完了するまで待機
            output_task.wait_until_done(timeout=wait_duration)
            
            # # タスクを終了（いらない？）
            # output_task.stop()

    except Exception:
        with nidaqmx.Task() as output_task:
            # 0を出力
            output_task.ao_channels.add_ao_voltage_chan(f"{device_name}/{ao_channel}")
            output_task.write(np.zeros(1), auto_start=True)