#coding:utf-8
"""
圧縮ファイルを解凍
ディレクトリ内の複数wavファイルを一括で処理
短時間フーリエ変換(stft)、図を出力
FFTの類似度を算出
RMS算出
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
import zipfile  #圧縮解凍ライブラリ
import cv2  #画像処理ライブラリ
import schedule  #定期実行ライブラリ


#FFT検出強度のフィルタリング
noise_reduction_filters = 0
#カラーバーのレンジ指定
vmin = -6
vmax = 6

t00 = time.time()
path = "/home/pi/Documents/admp441_data/"  #ディレクトリ先を変数pathに格納(データの格納先デレクトリを読み出すときに使用する)
path2 = "/home/pi/Documents/admp441_data/Save_wavfile/"
path3 = "/home/pi/Documents/admp441_data/uzip" 
path_FS = "/home/pi/Documents/admp441_data/FFT_data/FS/"
path1000Hz = "/home/pi/Documents/admp441_data/FFT_data/1000Hz/"
path4000Hz = "/home/pi/Documents/admp441_data/FFT_data/4000Hz/"
path8000Hz = "/home/pi/Documents/admp441_data/FFT_data/8000Hz/"
path12000Hz = "/home/pi/Documents/admp441_data/FFT_data/12000Hz/"
path16000Hz = "/home/pi/Documents/admp441_data/FFT_data/16000Hz/"
path20000Hz = "/home/pi/Documents/admp441_data/FFT_data/20000Hz/"

def Unzip():
    """解凍"""
    zipFile_List = glob.glob(path + "*.zip")
    for extractedfile in natsorted(zipFile_List):
        with zipfile.ZipFile(extractedfile) as unzipfile:
            unzipfile.extractall(path)
    for extractedfile in natsorted(zipFile_List):
        shutil.move(extractedfile, path3)

    """wavファイルからデータ解析"""
    t0 = time.time()
    #ファイルの名前をタイムスタンプ化する
    global timename
    timestamp = datetime.today()
    timename = timestamp.strftime("%Y%m%d%H%M%S")
    t1 = time.time()
    #wavファイルの読み込み
    global wavfile_A
    global fs_A
    global audio_signal_A
    global rms_A
    global spectrum_A
    global frequency_A
    global freqs
    global times
    global Sx
    """wavファイル抽出"""
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
            """FullScall"""
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
            """画像の読み込み"""
            #デフォルト画像の読み込み
            img_DFT = cv2.imread(path_FS + "/ReferenceData/" + "NT43_pump1_20210114.png")  #".png"の中にリファレンスのファイル名を入力
            #テンプレート画像の読み込み
            Template_File = glob.glob(path_FS + "*.png")
            for TEMP_File in natsorted(Template_File):
                img_TEMP = cv2.imread(TEMP_File)
                #テンプレートマッチングNCC（Normalized Cross Correlation正規化相互相関係数）
                method =cv2.TM_CCOEFF_NORMED
                #テンプレートマッチング算出
                result = cv2.matchTemplate(img_TEMP, img_DFT, cv2.TM_CCOEFF_NORMED)
                #最小値、最大値、座標を取得
                min_value, max_value, min_loc, max_loc = cv2.minMaxLoc(result)
                #ファイル名、類似度を格納
                RESULT = [os.path.splitext(os.path.basename(TEMP_File))[0],round(max_value,4)]
                #header = ["data", "TM_value"]
                
                #csv
                with open(path + timename + "_FS" + ".csv", "a", newline="", encoding="utf-8") as f:
                    writer = csv.writer(f)
                    #writer.writerow(header)
                    writer.writerows([RESULT])
                #pngファイル削除
                os.remove(TEMP_File)
                t9 = time.time()
            
            """1000Hz"""
            plt.pcolormesh(times, freqs, np.log10(Sx), cmap='jet', vmin=vmin, vmax=vmax, shading="gouraud")
            plt.ylim([0, 1000])
            #軸ラベル表示無しにするコマンド
            plt.xticks([])
            plt.yticks([])
            #グラフ余白なしにするコマンド
            plt.subplots_adjust(left=0, right=1, bottom=0, top=1)
            name, ext = os.path.splitext(audiofile)
            ext = ".png"
            out_path_1000Hz = os.path.join(*[path, name+"_1000Hz" + ext])
            plt.savefig(out_path_1000Hz)
            plt.close()
            shutil.move(out_path_1000Hz, path1000Hz)
            t10 = time.time()
            """画像の読み込み"""
            #デフォルト画像の読み込み
            img_DFT1000 = cv2.imread(path1000Hz + "/ReferenceData/" + "NT43_pump1_20210114_1000Hz.png")  #".png"の中にリファレンスのファイル名を入力
            #テンプレート画像の読み込み
            Template_File1000 = glob.glob(path1000Hz + "*.png")
            for TEMP_File1000 in natsorted(Template_File1000):
                img_TEMP1000 = cv2.imread(TEMP_File1000)
                #テンプレートマッチングNCC（Normalized Cross Correlation正規化相互相関係数）
                method =cv2.TM_CCOEFF_NORMED
                #テンプレートマッチング算出
                result1000 = cv2.matchTemplate(img_TEMP1000, img_DFT1000, cv2.TM_CCOEFF_NORMED)
                #最小値、最大値、座標を取得
                min_value1000, max_value1000, min_loc1000, max_loc1000 = cv2.minMaxLoc(result1000)
                #ファイル名、類似度を格納
                RESULT1000 = [os.path.splitext(os.path.basename(TEMP_File1000))[0],round(max_value1000,4)]
        
                #csv
                with open(path + timename+ "_1000Hz" + ".csv", "a", newline="", encoding="utf-8") as f1000:
                    writer = csv.writer(f1000)
                    writer.writerows([RESULT1000])
                #pngファイル削除
                os.remove(TEMP_File1000)
                t11 = time.time()
            
            
            """4000Hz"""
            plt.pcolormesh(times, freqs, np.log10(Sx), cmap='jet', vmin=vmin, vmax=vmax, shading="gouraud")
            plt.ylim([0, 4000])
            #軸ラベル表示無しにするコマンド
            plt.xticks([])
            plt.yticks([])
            #グラフ余白なしにするコマンド
            plt.subplots_adjust(left=0, right=1, bottom=0, top=1)
            name, ext = os.path.splitext(audiofile)
            ext = ".png"
            out_path_4000Hz = os.path.join(*[path, name+"_4000Hz" + ext])
            plt.savefig(out_path_4000Hz)
            plt.close()
            shutil.move(out_path_4000Hz, path4000Hz)
            t20 = time.time()
            """画像の読み込み"""
            #デフォルト画像の読み込み
            img_DFT4000 = cv2.imread(path4000Hz + "/ReferenceData/" + "NT43_pump1_20210114_4000Hz.png")  #".png"の中にリファレンスのファイル名を入力
            #テンプレート画像の読み込み
            Template_File4000 = glob.glob(path4000Hz + "*.png")
            for TEMP_File4000 in natsorted(Template_File4000):
                img_TEMP4000 = cv2.imread(TEMP_File4000)
                #テンプレートマッチングNCC（Normalized Cross Correlation正規化相互相関係数）
                method =cv2.TM_CCOEFF_NORMED
                #テンプレートマッチング算出
                result4000 = cv2.matchTemplate(img_TEMP4000, img_DFT4000, cv2.TM_CCOEFF_NORMED)
                #最小値、最大値、座標を取得
                min_value4000, max_value4000, min_loc4000, max_loc4000 = cv2.minMaxLoc(result4000)
                #ファイル名、類似度を格納
                RESULT4000 = [os.path.splitext(os.path.basename(TEMP_File4000))[0],round(max_value4000,4)]
        
                #csv
                with open(path + timename + "_4000Hz" + ".csv", "a", newline="", encoding="utf-8") as f4000:
                    writer = csv.writer(f4000)
                    writer.writerows([RESULT4000])
                #pngファイル削除
                os.remove(TEMP_File4000)
                t21 = time.time()
            
            
            """8000Hz"""
            plt.pcolormesh(times, freqs, np.log10(Sx), cmap='jet', vmin=vmin, vmax=vmax, shading="gouraud")
            plt.ylim([4000, 8000])
            #軸ラベル表示無しにするコマンド
            plt.xticks([])
            plt.yticks([])
            #グラフ余白なしにするコマンド
            plt.subplots_adjust(left=0, right=1, bottom=0, top=1)
            name, ext = os.path.splitext(audiofile)
            ext = ".png"
            out_path_8000Hz = os.path.join(*[path, name+"_8000Hz" + ext])
            plt.savefig(out_path_8000Hz)
            plt.close()
            shutil.move(out_path_8000Hz, path8000Hz)
            t30 = time.time()
            """画像の読み込み"""
            #デフォルト画像の読み込み
            img_DFT8000 = cv2.imread(path8000Hz + "/ReferenceData/" + "NT43_pump1_20210114_8000Hz.png")  #".png"の中にリファレンスのファイル名を入力
            #テンプレート画像の読み込み
            Template_File8000 = glob.glob(path8000Hz + "*.png")
            for TEMP_File8000 in natsorted(Template_File8000):
                img_TEMP8000 = cv2.imread(TEMP_File8000)
                #テンプレートマッチングNCC（Normalized Cross Correlation正規化相互相関係数）
                method =cv2.TM_CCOEFF_NORMED
                #テンプレートマッチング算出
                result8000 = cv2.matchTemplate(img_TEMP8000, img_DFT8000, cv2.TM_CCOEFF_NORMED)
                #最小値、最大値、座標を取得
                min_value8000, max_value8000, min_loc8000, max_loc8000 = cv2.minMaxLoc(result8000)
                #ファイル名、類似度を格納
                RESULT8000 = [os.path.splitext(os.path.basename(TEMP_File8000))[0],round(max_value8000,4)]
        
                #csv
                with open(path + timename + "_8000Hz" + ".csv", "a", newline="", encoding="utf-8") as f8000:
                    writer = csv.writer(f8000)
                    writer.writerows([RESULT8000])
                #pngファイル削除
                os.remove(TEMP_File8000)
                t31 = time.time()
            
            """12000Hz"""
            plt.pcolormesh(times, freqs, np.log10(Sx), cmap='jet', vmin=vmin, vmax=vmax, shading="gouraud")
            plt.ylim([8000, 12000])
            #軸ラベル表示無しにするコマンド
            plt.xticks([])
            plt.yticks([])
            #グラフ余白なしにするコマンド
            plt.subplots_adjust(left=0, right=1, bottom=0, top=1)
            name, ext = os.path.splitext(audiofile)
            ext = ".png"
            out_path_12000Hz = os.path.join(*[path, name+"_12000Hz" + ext])
            plt.savefig(out_path_12000Hz)
            plt.close()
            shutil.move(out_path_12000Hz, path12000Hz)
            t40 = time.time()
            """画像の読み込み"""
            #デフォルト画像の読み込み
            img_DFT12000 = cv2.imread(path12000Hz + "/ReferenceData/" + "NT43_pump1_20210114_12000Hz.png")  #".png"の中にリファレンスのファイル名を入力
            #テンプレート画像の読み込み
            Template_File12000 = glob.glob(path12000Hz + "*.png")
            for TEMP_File12000 in natsorted(Template_File12000):
                img_TEMP12000 = cv2.imread(TEMP_File12000)
                #テンプレートマッチングNCC（Normalized Cross Correlation正規化相互相関係数）
                method =cv2.TM_CCOEFF_NORMED
                #テンプレートマッチング算出
                result12000 = cv2.matchTemplate(img_TEMP12000, img_DFT12000, cv2.TM_CCOEFF_NORMED)
                #最小値、最大値、座標を取得
                min_value12000, max_value12000, min_loc12000, max_loc12000 = cv2.minMaxLoc(result12000)
                #ファイル名、類似度を格納
                RESULT12000 = [os.path.splitext(os.path.basename(TEMP_File12000))[0],round(max_value12000,4)]
        
                #csv
                with open(path + timename + "_12000Hz" + ".csv", "a", newline="", encoding="utf-8") as f12000:
                    writer = csv.writer(f12000)
                    writer.writerows([RESULT12000])
                #pngファイル削除
                os.remove(TEMP_File12000)
                t41 = time.time()
            
            """16000Hz"""
            plt.pcolormesh(times, freqs, np.log10(Sx), cmap='jet', vmin=vmin, vmax=vmax, shading="gouraud")
            plt.ylim([12000, 16000])
            #軸ラベル表示無しにするコマンド
            plt.xticks([])
            plt.yticks([])
            #グラフ余白なしにするコマンド
            plt.subplots_adjust(left=0, right=1, bottom=0, top=1)
            name, ext = os.path.splitext(audiofile)
            ext = ".png"
            out_path_16000Hz = os.path.join(*[path, name+"_16000Hz" + ext])
            plt.savefig(out_path_16000Hz)
            plt.close()
            shutil.move(out_path_16000Hz, path16000Hz)
            t50 = time.time()
            """画像の読み込み"""
            #デフォルト画像の読み込み
            img_DFT16000 = cv2.imread(path16000Hz + "/ReferenceData/" + "NT43_pump1_20210114_16000Hz.png")  #".png"の中にリファレンスのファイル名を入力
            #テンプレート画像の読み込み
            Template_File16000 = glob.glob(path16000Hz + "*.png")
            for TEMP_File16000 in natsorted(Template_File16000):
                img_TEMP16000 = cv2.imread(TEMP_File16000)
                #テンプレートマッチングNCC（Normalized Cross Correlation正規化相互相関係数）
                method =cv2.TM_CCOEFF_NORMED
                #テンプレートマッチング算出
                result16000 = cv2.matchTemplate(img_TEMP16000, img_DFT16000, cv2.TM_CCOEFF_NORMED)
                #最小値、最大値、座標を取得
                min_value16000, max_value16000, min_loc16000, max_loc16000 = cv2.minMaxLoc(result16000)
                #ファイル名、類似度を格納
                RESULT16000 = [os.path.splitext(os.path.basename(TEMP_File16000))[0],round(max_value16000,4)]
        
                #csv
                with open(path + timename + "_16000Hz" + ".csv", "a", newline="", encoding="utf-8") as f16000:
                    writer = csv.writer(f16000)
                    writer.writerows([RESULT16000])
                #pngファイル削除
                os.remove(TEMP_File16000)
                t51 = time.time()
            
            """20000Hz"""
            plt.pcolormesh(times, freqs, np.log10(Sx), cmap='jet', vmin=vmin, vmax=vmax, shading="gouraud")
            plt.ylim([16000, 20000])
            #軸ラベル表示無しにするコマンド
            plt.xticks([])
            plt.yticks([])
            #グラフ余白なしにするコマンド
            plt.subplots_adjust(left=0, right=1, bottom=0, top=1)
            name, ext = os.path.splitext(audiofile)
            ext = ".png"
            out_path_20000Hz = os.path.join(*[path, name+"_20000Hz" + ext])
            plt.savefig(out_path_20000Hz)
            plt.close()
            shutil.move(out_path_20000Hz, path20000Hz)
            t60 = time.time()
            """画像の読み込み"""
            #デフォルト画像の読み込み
            img_DFT20000 = cv2.imread(path20000Hz + "/ReferenceData/" + "NT43_pump1_20210114_20000Hz.png")  #".png"の中にリファレンスのファイル名を入力
            #テンプレート画像の読み込み
            Template_File20000 = glob.glob(path20000Hz + "*.png")
            for TEMP_File20000 in natsorted(Template_File20000):
                img_TEMP20000 = cv2.imread(TEMP_File20000)
                #テンプレートマッチングNCC（Normalized Cross Correlation正規化相互相関係数）
                method =cv2.TM_CCOEFF_NORMED
                #テンプレートマッチング算出
                result20000 = cv2.matchTemplate(img_TEMP20000, img_DFT20000, cv2.TM_CCOEFF_NORMED)
                #最小値、最大値、座標を取得
                min_value20000, max_value20000, min_loc20000, max_loc20000 = cv2.minMaxLoc(result20000)
                #ファイル名、類似度を格納
                RESULT20000 = [os.path.splitext(os.path.basename(TEMP_File20000))[0],round(max_value20000,4)]
        
                #csv
                with open(path + timename + "_20000Hz" + ".csv", "a", newline="", encoding="utf-8") as f20000:
                    writer = csv.writer(f20000)
                    writer.writerows([RESULT20000])
                #pngファイル削除
                os.remove(TEMP_File20000)
                t61 = time.time()
                
            #ファイル名、類似度を格納
            RESULT = [os.path.splitext(os.path.basename(wavfile_A))[0],round(rms_A,3)]
            #csv
            with open(path + timename + "_RMS" + ".csv", "a", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerows([RESULT])
            t70 = time.time()

    for audiofile in natsorted(File_List):
        os.remove(audiofile)
    t71 = time.time()
    print("finish "+timename)


#関数の読み出しコマンド
#schedule.every().day.at("00:00").do(Unzip)
#schedule.every(1).minutes.do(Unzip)
schedule.every(1).hour.do(Unzip)

while True:
    #定期実行の読み出し
    schedule.run_pending()
#except KeyboardInterrupt:
#print("FINISH!")
