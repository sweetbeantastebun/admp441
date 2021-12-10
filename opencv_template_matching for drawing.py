#coding:utf-8
"""
ディレクトリ内の複数wavファイルを一括で処理
FFT図の類似度を算出
"""
import time  #タイムカウントに使用するライブラリ
import numpy as np #行列、配列計算、FFT化するライブラリ
from scipy import signal  #信号処理や統計を使用するライブラリ
import matplotlib.pyplot as plt  #グラフを作成するライブラリ
from datetime import datetime  #タイムスタンプを実行するライブラリ
import csv  #csvを作成するライブラリ
import os  #ファイルやディレクトリをパス操作するライブラリ
import shutil  #ファイル、ディレクトリの移動、コピーするライブラリ
import glob  #複数のファイルを選択するライブラリ
import pandas as  pd  #数式、配列を操作するライブラリ
import cv2  #画像処理ライブラリ
from natsort import natsorted  #数字の順番に並べ替えるライブラリ（自然順アルゴリズム）


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


def Matching_FS():
    global t0
    global t1
    t0 = time.time()
    #ファイルの名前をタイムスタンプ化する
    global filename_A
    timestamp = datetime.today()
    csvFileName_A = timestamp.strftime("%Y%m%d%H%M%S")
    t1 = time.time()
    global t2
    global t3
    t2 = time.time()
    #画像の読み込み
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
        RESULT = [os.path.basename(TEMP_File),round(max_value,4)]
        #header = ["data", "TM_value"]
        #csv
        with open(path + csvFileName_A + "_FS" + ".csv", "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            #writer.writerow(header)
            writer.writerows([RESULT])
        #pngファイル削除
        os.remove(TEMP_File)
        t3 = time.time()


def Matching_1000Hz():
    global t10
    global t11
    t10 = time.time()
    #ファイルの名前をタイムスタンプ化する
    global filename_A
    timestamp = datetime.today()
    csvFileName_A = timestamp.strftime("%Y%m%d%H%M%S")
    t11 = time.time()
    global t12
    global t13
    t12 = time.time()
    #画像の読み込み
    #デフォルト画像の読み込み
    img_DFT = cv2.imread(path1000Hz + "/ReferenceData/" + "NT43_pump1_20210114_1000Hz.png")  #".png"の中にリファレンスのファイル名を入力
    #テンプレート画像の読み込み
    Template_File = glob.glob(path1000Hz + "*.png")
    for TEMP_File in natsorted(Template_File):
        img_TEMP = cv2.imread(TEMP_File)
        #テンプレートマッチングNCC（Normalized Cross Correlation正規化相互相関係数）
        method =cv2.TM_CCOEFF_NORMED
        #テンプレートマッチング算出
        result = cv2.matchTemplate(img_TEMP, img_DFT, cv2.TM_CCOEFF_NORMED)
        #最小値、最大値、座標を取得
        min_value, max_value, min_loc, max_loc = cv2.minMaxLoc(result)
        #ファイル名、類似度を格納
        RESULT = [os.path.basename(TEMP_File),round(max_value,4)]
        
        #csv
        with open(path + csvFileName_A + "_1000Hz" + ".csv", "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerows([RESULT])
        #pngファイル削除
        os.remove(TEMP_File)
        t13 = time.time()


def Matching_4000Hz():
    global t20
    global t21
    t20 = time.time()
    #ファイルの名前をタイムスタンプ化する
    global filename_A
    timestamp = datetime.today()
    csvFileName_A = timestamp.strftime("%Y%m%d%H%M%S")
    t21 = time.time()
    global t22
    global t23
    t22 = time.time()
    #画像の読み込み
    #デフォルト画像の読み込み
    img_DFT = cv2.imread(path4000Hz + "/ReferenceData/" + "NT43_pump1_20210114_4000Hz.png")  #".png"の中にリファレンスのファイル名を入力
    #テンプレート画像の読み込み
    Template_File = glob.glob(path4000Hz + "*.png")
    for TEMP_File in natsorted(Template_File):
        img_TEMP = cv2.imread(TEMP_File)
        #テンプレートマッチングNCC（Normalized Cross Correlation正規化相互相関係数）
        method =cv2.TM_CCOEFF_NORMED
        #テンプレートマッチング算出
        result = cv2.matchTemplate(img_TEMP, img_DFT, cv2.TM_CCOEFF_NORMED)
        #最小値、最大値、座標を取得
        min_value, max_value, min_loc, max_loc = cv2.minMaxLoc(result)
        #ファイル名、類似度を格納
        RESULT = [os.path.basename(TEMP_File),round(max_value,4)]
        
        #csv
        with open(path + csvFileName_A + "_4000Hz" + ".csv", "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerows([RESULT])
        #pngファイル削除
        os.remove(TEMP_File)
        t23 = time.time()


def Matching_8000Hz():
    global t30
    global t31
    t30 = time.time()
    #ファイルの名前をタイムスタンプ化する
    global filename_A
    timestamp = datetime.today()
    csvFileName_A = timestamp.strftime("%Y%m%d%H%M%S")
    t31 = time.time()
    global t32
    global t33
    t32 = time.time()
    #画像の読み込み
    #デフォルト画像の読み込み
    img_DFT = cv2.imread(path8000Hz + "/ReferenceData/" + "NT43_pump1_20210114_8000Hz.png")  #".png"の中にリファレンスのファイル名を入力
    #テンプレート画像の読み込み
    Template_File = glob.glob(path8000Hz + "*.png")
    for TEMP_File in natsorted(Template_File):
        img_TEMP = cv2.imread(TEMP_File)
        #テンプレートマッチングNCC（Normalized Cross Correlation正規化相互相関係数）
        method =cv2.TM_CCOEFF_NORMED
        #テンプレートマッチング算出
        result = cv2.matchTemplate(img_TEMP, img_DFT, cv2.TM_CCOEFF_NORMED)
        #最小値、最大値、座標を取得
        min_value, max_value, min_loc, max_loc = cv2.minMaxLoc(result)
        #ファイル名、類似度を格納
        RESULT = [os.path.basename(TEMP_File),round(max_value,4)]
        
        #csv
        with open(path + csvFileName_A + "_8000Hz" + ".csv", "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerows([RESULT])
        #pngファイル削除
        os.remove(TEMP_File)
        t33 = time.time()


def Matching_12000Hz():
    global t40
    global t41
    t40 = time.time()
    #ファイルの名前をタイムスタンプ化する
    global filename_A
    timestamp = datetime.today()
    csvFileName_A = timestamp.strftime("%Y%m%d%H%M%S")
    t41 = time.time()
    global t42
    global t43
    t42 = time.time()
    #画像の読み込み
    #デフォルト画像の読み込み
    img_DFT = cv2.imread(path12000Hz + "/ReferenceData/" + "NT43_pump1_20210114_12000Hz.png")  #".png"の中にリファレンスのファイル名を入力
    #テンプレート画像の読み込み
    Template_File = glob.glob(path12000Hz + "*.png")
    for TEMP_File in natsorted(Template_File):
        img_TEMP = cv2.imread(TEMP_File)
        #テンプレートマッチングNCC（Normalized Cross Correlation正規化相互相関係数）
        method =cv2.TM_CCOEFF_NORMED
        #テンプレートマッチング算出
        result = cv2.matchTemplate(img_TEMP, img_DFT, cv2.TM_CCOEFF_NORMED)
        #最小値、最大値、座標を取得
        min_value, max_value, min_loc, max_loc = cv2.minMaxLoc(result)
        #ファイル名、類似度を格納
        RESULT = [os.path.basename(TEMP_File),round(max_value,4)]
        
        #csv
        with open(path + csvFileName_A + "_12000Hz" + ".csv", "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerows([RESULT])
        #pngファイル削除
        os.remove(TEMP_File)
        t43 = time.time()


def Matching_16000Hz():
    global t50
    global t51
    t50 = time.time()
    #ファイルの名前をタイムスタンプ化する
    global filename_A
    timestamp = datetime.today()
    csvFileName_A = timestamp.strftime("%Y%m%d%H%M%S")
    t51 = time.time()
    global t52
    global t53
    t52 = time.time()
    #画像の読み込み
    #デフォルト画像の読み込み
    img_DFT = cv2.imread(path16000Hz + "/ReferenceData/" + "NT43_pump1_20210114_16000Hz.png")  #".png"の中にリファレンスのファイル名を入力
    #テンプレート画像の読み込み
    Template_File = glob.glob(path16000Hz + "*.png")
    for TEMP_File in natsorted(Template_File):
        img_TEMP = cv2.imread(TEMP_File)
        #テンプレートマッチングNCC（Normalized Cross Correlation正規化相互相関係数）
        method =cv2.TM_CCOEFF_NORMED
        #テンプレートマッチング算出
        result = cv2.matchTemplate(img_TEMP, img_DFT, cv2.TM_CCOEFF_NORMED)
        #最小値、最大値、座標を取得
        min_value, max_value, min_loc, max_loc = cv2.minMaxLoc(result)
        #ファイル名、類似度を格納
        RESULT = [os.path.basename(TEMP_File),round(max_value,4)]
        
        #csv
        with open(path + csvFileName_A + "_16000Hz" + ".csv", "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerows([RESULT])
        #pngファイル削除
        os.remove(TEMP_File)
        t53 = time.time()


def Matching_20000Hz():
    global t60
    global t61
    t60 = time.time()
    #ファイルの名前をタイムスタンプ化する
    global filename_A
    timestamp = datetime.today()
    csvFileName_A = timestamp.strftime("%Y%m%d%H%M%S")
    t61 = time.time()
    global t62
    global t63
    t62 = time.time()
    #画像の読み込み
    #デフォルト画像の読み込み
    img_DFT = cv2.imread(path20000Hz + "/ReferenceData/" + "NT43_pump1_20210114_20000Hz.png")  #".png"の中にリファレンスのファイル名を入力
    #テンプレート画像の読み込み
    Template_File = glob.glob(path20000Hz + "*.png")
    for TEMP_File in natsorted(Template_File):
        img_TEMP = cv2.imread(TEMP_File)
        #テンプレートマッチングNCC（Normalized Cross Correlation正規化相互相関係数）
        method =cv2.TM_CCOEFF_NORMED
        #テンプレートマッチング算出
        result = cv2.matchTemplate(img_TEMP, img_DFT, cv2.TM_CCOEFF_NORMED)
        #最小値、最大値、座標を取得
        min_value, max_value, min_loc, max_loc = cv2.minMaxLoc(result)
        #ファイル名、類似度を格納
        RESULT = [os.path.basename(TEMP_File),round(max_value,4)]
        
        #csv
        with open(path + csvFileName_A + "_20000Hz" + ".csv", "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerows([RESULT])
        #pngファイル削除
        os.remove(TEMP_File)
        t63 = time.time()

Matching_FS()
Matching_1000Hz()
Matching_4000Hz()
Matching_8000Hz()
Matching_12000Hz()
Matching_16000Hz()
Matching_20000Hz()
print("finish")
#except KeyboardInterrupt:
#print("FINISH!")
