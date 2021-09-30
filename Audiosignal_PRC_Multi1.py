# coding: utf-8
import time  #タイムカウントに使用するライブラリ
import subprocess  #Terminalを実行するライブラリ
import numpy as np #配列計算、FFT化するライブラリ
import wave  #wavファイルの読み書きするライブラリ
import csv  #csvを作成するライブラリ
import os  #ファイルやディレクトリをパス操作するライブラリ
import matplotlib.pyplot as plt  #グラフを作成するライブラリ
from datetime import datetime  #タイムスタンプを実行するライブラリ
from threading import Thread  #スレッド処理するライブラリ
import concurrent.futures
from concurrent.futures import ThreadPoolExecutor, as_completed  #複数の処理を並列実行するためのライブラリ
import shutil  #ファイル、ディレクトリの移動、コピーするライブラリ
import glob  #複数のファイルを選択するライブラリ
import pandas as  pd  #数式、配列を操作するライブラリ
import psutil  #メモリ、CPUの使用率をモニターするライブラリ

#グラフのリアルタイムプロットの更新時間数
Loop_count_Value1 = 59
Loop_count_Value2 = 1000
#しきい値を指定
threshold_value_MAX = 0.097
threshold_value_MIN = 0.005
#FFT検出強度のフィルタリング
noise_reduction_filters = 10

t00 = time.time()
#ディレクトリ先を変数pathに格納(データの格納先デレクトリを読み出すときに使用する)
path_A1 = "/home/pi/Documents/admp441_data_A/"  
path_A2 = "/home/pi/Documents/admp441_data_A/Save_wavfile"
path_B1 = "/home/pi/Documents/admp441_data_B/"  
path_B2 = "/home/pi/Documents/admp441_data_B/Save_wavfile"

def Recording_A():
    global t0
    global t1
    t0 = time.time()
    #ファイルの名前をタイムスタンプ化する
    global filename_A
    timestamp = datetime.today()
    filename_A = str(timestamp.year) + str(timestamp.month) + str(timestamp.day) + "_" + str(timestamp.hour) + ":" + str(timestamp.minute) + ":" + str(timestamp.second)
    #録音実行（16ビット量子化、44.1kHz）
    record = "arecord -d 1 -f S16_LE -r 44100 /home/pi/Documents/admp441_data_A/"+filename_A+".wav"
    subprocess.call(record, shell=True)
    t1 = time.time()
    #wavファイルの読み込み
    global t3
    global t4
    global t5
    global wavfile_A
    global fs_A
    global audio_signal_A
    global rms_A
    wavfile_A = path_A1 + filename_A + ".wav"
    wr = wave.open(wavfile_A, "r")  #wavファイルの読み込み。ファイル開く。オブジェクト化。
    fs_A = wr.getframerate()  #サンプリング周波数。Wave_readのメソッド
    samples = wr.readframes(wr.getnframes())  #オーディオフレーム数を読み込み。Wave_readのメソッド（=処理）
    samples = np.frombuffer(samples, dtype="int16") / float((np.power(2, 16) / 2) - 1)  #符号付き整数型16ビットに正規化した配列へ変換する
    wr.close()  #読み込み終了。ファイルオブジェクトの終了。 
    t3 = time.time()
    #samplesを変数audio_signalとしてコピー
    audio_signal_A = samples.copy()
    #RMS
    rms_A = np.sqrt((audio_signal_A**2).mean())
    t4 = time.time()
    if rms_A is np.nan:
        rms_A == 0.001
    t5 = time.time()
    #print("Recording_A", t5-t0)

def Graph_A():
    global t10
    global t19
    global RMS_data
    global sample_of_numbers
    t10 = time.time()
    #RMS値と測定回数をリストに格納する
    RMS_data.append(round(rms_A,4))
    RMS_data.pop(0)
    sample_of_numbers.append(index_loop)
    sample_of_numbers.pop(0)
    #グラフ作成
    plt.ion()
    plt.clf()
    plt.cla()
    No1, = plt.plot(sample_of_numbers, RMS_data, lw=1)
    plt.xticks(fontsize = 8)
    plt.yticks(fontsize = 8)
    plt.xlabel("Sample Number", fontsize=8)
    plt.ylabel("RMS", fontsize=8)
    plt.grid(which="both")
    No1.set_data(sample_of_numbers, RMS_data)
    plt.xlim(sample_of_numbers[-Loop_count_Value1], sample_of_numbers[-1])
    plt.draw()
    plt.pause(0.01) 
    t11 = time.time()
    
    if rms_A >= threshold_value_MAX:
        plt.savefig("/home/pi/Documents/admp441_data/"+filename_A+"Maximum_value"".png")
        file =  filename_A + ".wav"
        shutil.copy(path_A1 + file , path_A2)  #wavファイルをコピーして指定ディレクトリへ移動
        #1サンプル中のMax値
        Maximum_audio_signal_A = np.max(audio_signal_A)
        #1サンプル中の波高率
        Wave_height_rate_A = rms_A / Maximum_audio_signal_A
        #csvファイルに書き込むフレーム作成
        header_names = [["Maximum_value", "Wave_height_rate", "RMS"],
        [round(Maximum_audio_signal_A,4), round(Wave_height_rate_A,4), round(rms_A,4)]]
        #csv作成
        with open("/home/pi/Documents/admp441_data/"+filename_A+"Maximum_value"+".csv", "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerows(header_names)
    """
    if rms_A <= threshold_value_MIN:
        plt.savefig("/home/pi/Documents/admp441_data/"+filename_A+"Minimum_value"".png")
        file =  filename_A + ".wav"
        shutil.copy(path_A1 + file , path_A2)  #wavファイルをコピーして指定ディレクトリへ移動
    """
    t15 = time.time()
    #wavファイル削除
    file = filename_A + ".wav"
    os.remove(path_A1 + file)
    t19 = time.time()
    #print("Greph_A", t19-t10)


def Recording_B():
    global t20
    global t21
    t20 = time.time()
    #ファイルの名前をタイムスタンプ化する
    global filename_B
    timestamp = datetime.today()
    filename_B = str(timestamp.year) + str(timestamp.month) + str(timestamp.day) + "_" + str(timestamp.hour) + ":" + str(timestamp.minute) + ":" + str(timestamp.second)
    #録音実行（16ビット量子化、44.1kHz）
    record = "arecord -d 1 -f S16_LE -r 44100 /home/pi/Documents/admp441_data_B/"+filename_B+".wav"
    subprocess.call(record, shell=True)
    t21 = time.time()
    #wavファイルの読み込み
    global t23
    global t24
    global t25
    global wavfile_B
    global fs_B
    global audio_signal_B
    global rms_B
    wavfile_B = path_B1 + filename_B + ".wav"
    wr = wave.open(wavfile_B, "r")  #wavファイルの読み込み。ファイル開く。オブジェクト化。
    fs_B = wr.getframerate()  #サンプリング周波数。Wave_readのメソッド（=処理）
    samples = wr.readframes(wr.getnframes())  #オーディオフレーム数を読み込み。Wave_readのメソッド（=処理）
    samples = np.frombuffer(samples, dtype="int16") / float((np.power(2, 16) / 2) - 1)  #符号付き整数型16ビットに正規化した配列へ変換する
    wr.close()  #読み込み終了。ファイルオブジェクトの終了。 
    t23 = time.time()
    #samplesを変数audio_signalとしてコピー
    audio_signal_B = samples.copy()
    """RMS"""
    rms_B = np.sqrt((audio_signal_B**2).mean())
    t24 = time.time()
    if rms_B is np.nan:
        rms_B == 0.001
    t25 = time.time()
    #print("Recording_B", t25-t20)
        
        
def Graph_B():
    global t30
    global t39
    global RMS_data
    global sample_of_numbers
    t30 = time.time()
    #RMS値と測定回数をリストに格納する
    RMS_data.append(round(rms_B,4))
    RMS_data.pop(0)
    sample_of_numbers.append(index_loop)
    sample_of_numbers.pop(0)
    #グラフ作成
    plt.ion()
    plt.clf()
    plt.cla()
    No1, = plt.plot(sample_of_numbers, RMS_data, lw=1)
    plt.xticks(fontsize = 8)
    plt.yticks(fontsize = 8)
    plt.xlabel("Sample Number", fontsize=8)
    plt.ylabel("RMS", fontsize=8)
    plt.grid(which="both")
    No1.set_data(sample_of_numbers, RMS_data)
    plt.xlim(sample_of_numbers[-Loop_count_Value1], sample_of_numbers[-1])
    plt.draw()
    plt.pause(0.01) 
    t33 = time.time()
    
    if rms_B >= threshold_value_MAX:
        plt.savefig("/home/pi/Documents/admp441_data/"+filename_B+"MAX_value"".png")
        file =  filename_B + ".wav"
        shutil.copy(path_B1 + file , path_B2)  #wavファイルをコピーして指定ディレクトリへ移動
        #1サンプル中のMax値
        Maximum_audio_signal_B = np.max(audio_signal_B)
        #1サンプル中の波高率
        Wave_height_rate_B = rms_B / Maximum_audio_signal_B
        #csvファイルに書き込むフレーム作成
        header_names = [["MAX_value", "Wave_height_rate", "RMS"],
        [round(Maximum_audio_signal_B,4), round(Wave_height_rate_B,4), round(rms_B,4)]]
        #csv作成
        with open("/home/pi/Documents/admp441_data/"+filename_B+"MAX_value"+".csv", "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerows(header_names)
    """
    if rms_B <= threshold_value_MIN:
        plt.savefig("/home/pi/Documents/admp441_data/"+filename_B+"MIN_value"".png")
        file =  filename_B + ".wav"
        shutil.copy(path_B1 + file , path_B2)  #wavファイルをコピーして指定ディレクトリへ移動
    """
    t38 = time.time()
    #wavファイル削除
    file = filename_B + ".wav"
    os.remove(path_B1 + file)
    t39 = time.time()
    #print("Greph_B", t39-t30)
    
    
    
def job_A():
    t40 = time.time()
    plt.clf()
    No1, = plt.plot(sample_of_numbers, RMS_data, lw=1)
    plt.xlim(sample_of_numbers[-Loop_count_Value2], sample_of_numbers[-1])
    plt.ylim(0, 0.05)
    plt.xticks(fontsize = 8)
    plt.yticks(fontsize = 8)
    plt.xlabel("Sample Number", fontsize=8)
    plt.ylabel("RMS", fontsize=8)
    plt.grid(which="both")
    No1.set_data(sample_of_numbers, RMS_data)
    plt.subplots_adjust(wspace=0.3, hspace=0.3)  #隣接グラフとの隙間
    plt.savefig("/home/pi/Documents/admp441_data/"+filename_A+"cron"".png")
    plt.close()
    t41 = time.time()
    #csv作成、出力
    #期間中のMax値
    Maximum_value = np.max(RMS_data)
    #期間中のMin値
    Minimum_value = np.min(RMS_data)
    #期間中のMean値
    Average_value = np.mean(RMS_data)
    #期間中のRMS値の波高率
    Wave_height_rate_RMS = Maximum_value / Average_value
    #波形の個数を数値化処理
    data_frame = pd.DataFrame(RMS_data, columns=["spectrum"])  #データフレーム作成
    peeks = (data_frame["spectrum"] >= threshold_value_MAX).sum()  #しきい値以上のピーク検体数をカウント
    #memory,cpu,harddiskの使用率をモニタ
    memory = psutil.virtual_memory()  #memory使用率の出力
    cpu = psutil.cpu_percent(interval = 1)  #cpu使用率を出力
    disk = psutil.disk_usage("/")  #disk容量
    #csvファイルに書き込むフレーム作成
    header_names = [["Maximum_value", "Minimum_value", "Average_value", "Wave_height_rate", "number_of_peeks", "memory.percent", "cpu", "disk.percent"],
    [round(Maximum_value,4), round(Minimum_value,4), round(Average_value,4), round(Wave_height_rate_RMS,4), peeks, memory.percent, cpu, disk.percent]]
    #csv作成
    with open("/home/pi/Documents/admp441_data/"+filename_A+"cron"+".csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerows(header_names) 
    
    #録音実行（16ビット量子化、44.1kHz）
    record = "arecord -d 1 -f S16_LE -r 44100 /home/pi/Documents/admp441_data/"+filename_A+".wav"
    subprocess.call(record, shell=True)
    t42 = time.time()
    #print("job_A", t42-t40)

RMS_data = []
sample_of_numbers = []
index_loop = 1
while index_loop <= Loop_count_Value2:
    Recording_A()
    RMS_data.append(rms_A)
    sample_of_numbers.append(index_loop)
    #wavファイル削除
    file_A = filename_A + ".wav"
    os.remove(path_A1 + file_A)
    index_loop += 1
    Recording_B()
    RMS_data.append(rms_B)
    sample_of_numbers.append(index_loop)
    #wavファイル削除
    file_B = filename_B + ".wav"
    os.remove(path_B1 + file_B)
    index_loop += 1
    
 
Recording_A()
#ここから無限ループ。
#並列処理でレコード中に音声解析(FFT)を実行する。
#タスクを4つ(recording_AとB、FFT_AとB)作成し、
#recording_BとFFT_Aの組み合わせ(recording_B実行中にFFT_Aを処理)
#recording_AとFFT_Bの組み合わせ(recording_A実行中にFFT_Bを処理)
#で処理していく。
index_loop = Loop_count_Value1 + 1
while True:
    t100 = time.time()
    executor = concurrent.futures.ThreadPoolExecutor(max_workers=4)
    result_B = executor.submit(Recording_B()) #recording_Bを実行し、これを変数result_Bとしておく
    executor.submit(Graph_A()) #FFT_Aを実行する(上記と平行)
    as_completed([result_B]).__next__() #変数result_Bが終了したら、次に進む
    index_loop += 1
    t102 = time.time()
    result_A = executor.submit(Recording_A()) #recording_Aを実行し、これを変数result_Aとしておく
    executor.submit(Graph_B()) #FFT_Bを実行する(上記と平行)
    as_completed([result_A]).__next__() #変数result_Aが終了したら、次に進む
    index_loop += 1
    t104 = time.time()
    
    #定期実行処理
    if index_loop % Loop_count_Value2 == 0:
        job_A()
    """
    print("thread_1", t102-t100)
    print("thread_2", t104-t102)
    print("Record_A", t5-t0)
    print("Record_B", t25-t20)
    print("Graph_A", t19-t10)
    print("Graph_B", t39-t30)
    """
    """
    #memory使用率を出力
    memory = psutil.virtual_memory()
    print('memory.percent',memory.percent)
    #cpu使用率を出力
    cpu = psutil.cpu_percent(interval=1)
    print('cpu',cpu)
    #diskの容量を出力
    disk = psutil.disk_usage('/')
    print('disk.percent',disk.percent)                    
    """
