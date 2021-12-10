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
#import schedule

t00 = time.time()
path_A1 = "/home/pi/Documents/admp441_data_A/"  #ディレクトリ先を変数pathに格納(データの格納先デレクトリを読み出すときに使用する)

def Recording_A():
    global t0
    global t1
    global t2
    global t3
    global t4
    global t5
    global filename_A
    global rms_A
    global DATE
    global Value
    index = 0
    DATE = []
    Value = []
    while index < 30:
        t0 = time.time()
        #ファイルの名前をタイムスタンプ化する
        timestamp = datetime.today()
        filename_A = timestamp.strftime("%Y%m%d%H%M%S")
        #録音実行（16ビット量子化、44.1kHz）
        record = 'arecord -d 1 -f S16_LE -r 44100 /home/pi/Documents/admp441_data_A/'+filename_A+'.wav'
        subprocess.call(record, shell=True)
        t1 = time.time()
        #wavファイルの読み込み
        t2 = time.time()
        wavfile_A = path_A1 + filename_A + ".wav"
        wr = wave.open(wavfile_A, "r")  #wavファイルの読み込み。ファイル開く。オブジェクト化。
        fs_A = wr.getframerate()  #サンプリング周波数。Wave_readのメソッド（=処理）
        samples = wr.readframes(wr.getnframes())  #オーディオフレーム数を読み込み。Wave_readのメソッド（=処理）
        samples = np.frombuffer(samples, dtype="int16") / float((np.power(2, 16) / 2) - 1)  #符号付き整数型16ビットに正規化した配列へ変換する
        wr.close()  #読み込み終了。ファイルオブジェクトの終了。 
        t3 = time.time()
        #samplesを変数audio_signalとしてコピー
        audio_signal_A = samples.copy()
        #RMS
        rms_A = np.sqrt((audio_signal_A**2).mean())
        if rms_A is np.nan:
            rms_A == 0.001
        #print("RMS", round(rms_A,4))
        #リスト作成
        DATE.append(filename_A)
        Value.append(round(rms_A,4))
        #wavファイル削除
        file = filename_A + ".wav"
        os.remove(path_A1 + file)
        index += 1
        t5 = time.time()
        #print("Recording_A", t5-t0)
        
def job_A():
    t20 = time.time()
    #録音実行（16ビット量子化、44.1kHz）
    record = "arecord -d 1 -f S16_LE -r 44100 /home/pi/Documents/admp441_data/"+filename_A+".wav"
    subprocess.call(record, shell=True)
    t22 = time.time()
    #print("job_A", t22-t20)
"""
#１分毎に関数job_Bを実施
schedule.every(1).minutes.do(job_A)
#schedule.every(1).hour.do(job_A) 
"""
while True:
    Recording_A()
    #csv作成、出力
    df_RESHAPE = pd.DataFrame({"DATE":DATE, "RMS":Value})
    df_RESHAPE.to_csv("/home/pi/Documents/admp441_data/" +filename_A+ ".csv")
    Data_List = {filename_A : Value}
    Layout = pd.DataFrame(Data_List)
    aggregate = Layout.describe()
    aggregate = aggregate.round(4)
    aggregate.to_csv("/home/pi/Documents/admp441_data/"+filename_A+"AGR"+".csv")
    """
    #定期実行の読み出し
    schedule.run_pending()
    """
#except KeyboardInterrupt:
#print("FINISH!")
