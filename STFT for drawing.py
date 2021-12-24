#coding:utf-8
"""
ディレクトリ内の複数wavファイルを一括で処理
短時間フーリエ変換(stft)、図を出力
"""
import time  #タイムカウントに使用するライブラリ
import subprocess  #Terminalを実行するライブラリ
import wave  #wavファイルの読み書きするライブラリ
import numpy as np #行列、配列計算、FFT化するライブラリ
from scipy import signal  #信号処理や統計を使用するライブラリ
import matplotlib.pyplot as plt  #グラフを作成するライブラリ
from datetime import datetime  #タイムスタンプを実行するライブラリ
import csv  #csvを作成するライブラリ
import os  #ファイルやディレクトリをパス操作するライブラリ
import shutil  #ファイル、ディレクトリの移動、コピーするライブラリ
import glob  #複数のファイルを選択するライブラリ
import pandas as  pd  #数式、配列を操作するライブラリ
import psutil  #メモリ、CPUの使用率をモニターするライブラリ
from natsort import natsorted  #数字の順番に並べ替えるライブラリ（自然順アルゴリズム）

#FFT検出強度のフィルタリング
noise_reduction_filters = 0
#カラーバーのレンジ指定
vmin = -6
vmax = 6

t00 = time.time()
path = "/home/pi/Documents/admp441_data/"  #ディレクトリ先を変数pathに格納(データの格納先デレクトリを読み出すときに使用する)
path2 ="/home/pi/Documents/admp441_data/Save_wavfile/"
path_FS = "/home/pi/Documents/admp441_data/FFT_data/FS/"
path1000Hz = "/home/pi/Documents/admp441_data/FFT_data/1000Hz/"
path4000Hz = "/home/pi/Documents/admp441_data/FFT_data/4000Hz/"
path8000Hz = "/home/pi/Documents/admp441_data/FFT_data/8000Hz/"
path12000Hz = "/home/pi/Documents/admp441_data/FFT_data/12000Hz/"
path16000Hz = "/home/pi/Documents/admp441_data/FFT_data/16000Hz/"
path20000Hz = "/home/pi/Documents/admp441_data/FFT_data/20000Hz/"

def Drawing():
    global t0
    global t1
    t0 = time.time()
    #ファイルの名前をタイムスタンプ化する
    global filename_A
    timestamp = datetime.today()
    filename_A = timestamp.strftime("%Y%m%d%H%M%S")
    t1 = time.time()
    #wavファイルの読み込み
    global t2
    global t3
    global t4
    global t5
    global t6
    global wavfile_A
    global fs_A
    global audio_signal_A
    global rms_A
    global spectrum_A
    global frequency_A
    global freqs
    global times
    global Sx
    t2 = time.time()
    File_List = glob.glob(path + "*.wav")
    for audiofile in natsorted(File_List):
        wavfile_A = audiofile
        wr = wave.open(wavfile_A, "r")  #wavファイルの読み込み。ファイル開く。オブジェクト化。
        fs_A = wr.getframerate()  #サンプリング周波数。Wave_readのメソッド（=処理）
        samples = wr.readframes(wr.getnframes())  #オーディオフレーム数を読み込み。Wave_readのメソッド（=処理）
        samples_N = np.frombuffer(samples, dtype="int16")
        samples = np.frombuffer(samples, dtype="int16")  / float((np.power(2, 16) / 2) - 1)  #符号付き整数型16ビットに正規化した配列へ変換する
        audio_data_length = np.arange(0, len(samples))/float(fs_A) # 音声データの長さ(x軸)
        wr.close()  #読み込み終了。ファイルオブジェクトの終了。 
        t3 = time.time()
        #samplesを変数audio_signalとしてコピー
        audio_signal_A = samples.copy()
        """RMS"""
        rms_A = np.sqrt((audio_signal_A**2).mean())
        if rms_A is np.nan:
            pass
        else:
            #print("RMS", round(rms_A,4))
            t4= time.time()
            """FFT"""
            N = 8192  #サンプル数を指定 #録音10秒で4096データの周波数分解能は10Hz #8192=5Hz
            spectrum_A = np.fft.fft(samples[0:N])  #2次元配列(実部，虚部)
            frequency_A = np.fft.fftfreq(N, 1.0/fs_A)  #周波数軸の計算
            #フィルタリング機能
            spectrum_A[(spectrum_A < noise_reduction_filters)] = 0  #しきい値未満の振幅はゼロにする
            #グラフ準備
            spectrum_A = spectrum_A[:int(spectrum_A.shape[0]/2)]    #スペクトルがマイナスになるスペクトル要素の削除
            frequency_A = frequency_A[:int(frequency_A.shape[0]/2)]    #周波数がマイナスになる周波数要素の削除    
            t5 = time.time()
            #print("Recording_A", t5-t0)
            """STFT"""
            #フレーム数の指定
            NN = 8192
            #周波数、時間軸、スペクトル強度を算出する
            freqs, times, Sx = signal.spectrogram(samples_N, fs = fs_A, window = "hanning",
                                                  nperseg = NN,  #nperseg:分割数
                                                  noverlap = NN/8,  #フレームの重なり具合。
                                                  detrend = False, scaling = "spectrum") # スペクトログラム変数
            t6 = time.time()
            #print("signal_spectrogram", t6-t5)
        
            #グラフ作成
            #FullScall
            plt.pcolormesh(times, freqs, np.log10(Sx), cmap='jet', vmin=vmin, vmax=vmax, shading="gouraud")
            """
            #plt.ylim([0, 1000])
            plt.ylim([0, framerate/2])
            plt.ylabel("Frequency[Hz]", fontsize=10)
            plt.xlabel("Time[s]", fontsize=10)
            plt.xticks(fontsize = 9)
            plt.yticks(fontsize = 9)
            plt.colorbar(aspect=40, pad=0.02).set_label("SP[Pa]", fontsize=9)
            """
            #軸ラベル表示無しにするコマンド
            plt.xticks([])
            plt.yticks([])
            #グラフ余白なしにするコマンド
            plt.subplots_adjust(left=0, right=1, bottom=0, top=1)
            name, ext = os.path.splitext(audiofile)
            ext = ".png"
            out_path_FS = os.path.join(*[path, name + ext])
            plt.savefig(out_path_FS)
            plt.close()
            shutil.move(out_path_FS, path_FS)
            t8 = time.time()
            
            #1000Hz
            plt.pcolormesh(times, freqs, np.log10(Sx), cmap='jet', vmin=vmin, vmax=vmax, shading="gouraud")
            plt.ylim([0, 1000])
            #軸ラベル表示無しにするコマンド
            plt.xticks([])
            plt.yticks([])
            #グラフ余白なしにするコマンド
            plt.subplots_adjust(left=0, right=1, bottom=0, top=1)
            name, ext = os.path.splitext(audiofile)
            ext = ".png"
            out_path_1000Hz = os.path.join(*[path, name + ext])
            plt.savefig(out_path_1000Hz)
            plt.close()
            shutil.move(out_path_1000Hz, path1000Hz)
            t9 = time.time()
            
            #4000Hz
            plt.pcolormesh(times, freqs, np.log10(Sx), cmap='jet', vmin=vmin, vmax=vmax, shading="gouraud")
            plt.ylim([0, 4000])
            #軸ラベル表示無しにするコマンド
            plt.xticks([])
            plt.yticks([])
            #グラフ余白なしにするコマンド
            plt.subplots_adjust(left=0, right=1, bottom=0, top=1)
            name, ext = os.path.splitext(audiofile)
            ext = ".png"
            out_path_4000Hz = os.path.join(*[path, name + ext])
            plt.savefig(out_path_4000Hz)
            plt.close()
            shutil.move(out_path_4000Hz, path4000Hz)
            t10 = time.time()
            
            #8000Hz
            plt.pcolormesh(times, freqs, np.log10(Sx), cmap='jet', vmin=vmin, vmax=vmax, shading="gouraud")
            plt.ylim([4000, 8000])
            #軸ラベル表示無しにするコマンド
            plt.xticks([])
            plt.yticks([])
            #グラフ余白なしにするコマンド
            plt.subplots_adjust(left=0, right=1, bottom=0, top=1)
            name, ext = os.path.splitext(audiofile)
            ext = ".png"
            out_path_8000Hz = os.path.join(*[path, name + ext])
            plt.savefig(out_path_8000Hz)
            plt.close()
            shutil.move(out_path_8000Hz, path8000Hz)
            t11 = time.time()
            
            #12000Hz
            plt.pcolormesh(times, freqs, np.log10(Sx), cmap='jet', vmin=vmin, vmax=vmax, shading="gouraud")
            plt.ylim([8000, 12000])
            #軸ラベル表示無しにするコマンド
            plt.xticks([])
            plt.yticks([])
            #グラフ余白なしにするコマンド
            plt.subplots_adjust(left=0, right=1, bottom=0, top=1)
            name, ext = os.path.splitext(audiofile)
            ext = ".png"
            out_path_12000Hz = os.path.join(*[path, name + ext])
            plt.savefig(out_path_12000Hz)
            plt.close()
            shutil.move(out_path_12000Hz, path12000Hz)
            t12 = time.time()
            
            #16000Hz
            plt.pcolormesh(times, freqs, np.log10(Sx), cmap='jet', vmin=vmin, vmax=vmax, shading="gouraud")
            plt.ylim([12000, 16000])
            #軸ラベル表示無しにするコマンド
            plt.xticks([])
            plt.yticks([])
            #グラフ余白なしにするコマンド
            plt.subplots_adjust(left=0, right=1, bottom=0, top=1)
            name, ext = os.path.splitext(audiofile)
            ext = ".png"
            out_path_16000Hz = os.path.join(*[path, name + ext])
            plt.savefig(out_path_16000Hz)
            plt.close()
            shutil.move(out_path_16000Hz, path16000Hz)
            t12 = time.time()
            
            #20000Hz
            plt.pcolormesh(times, freqs, np.log10(Sx), cmap='jet', vmin=vmin, vmax=vmax, shading="gouraud")
            plt.ylim([16000, 20000])
            #軸ラベル表示無しにするコマンド
            plt.xticks([])
            plt.yticks([])
            #グラフ余白なしにするコマンド
            plt.subplots_adjust(left=0, right=1, bottom=0, top=1)
            name, ext = os.path.splitext(audiofile)
            ext = ".png"
            out_path_20000Hz = os.path.join(*[path, name + ext])
            plt.savefig(out_path_20000Hz)
            plt.close()
            shutil.move(out_path_20000Hz, path20000Hz)
            t14 = time.time()
            
            #ファイル名、類似度を格納
            RESULT = [os.path.splitext(os.path.basename(wavfile_A))[0],round(rms_A,3)]
            #csv
            with open(path + filename_A + "_RMS" + ".csv", "a", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerows([RESULT])
            t15 = time.time()
Drawing()
print("finish")
#except KeyboardInterrupt:
#print("FINISH!")
