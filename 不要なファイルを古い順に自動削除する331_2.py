#!/usr/bin/env python
# coding: utf-8
#プログラムコード構成
#フォルダ内のファイルをリスト化する。
#その中で対象ファイル(.wav)があれば、取り出して削除する。

import os  #ファイルやパスの操作をするライブラリ
import time  #タイムカウントに使用するライブラリ
from operator import itemgetter  #リストの並び替えるライブラリ

t00 = time.time()
path = '/home/pi/Documents/admp441_data/'  #一覧を取得したいディレクトリ先を指定

filelists = []  #データを入れる(append)空リストを作成
#print(os.listdir(path))
for file in os.listdir(path):  #フォルダ内のファイルを一覧にするコマンド
    print('-----------------------')
    print(file)
    base, ext = os.path.splitext(file)  #各要素(タプル)を変数base,extにそれぞれ分割して代入。base(ベースネーム,拡張子以外の部分)とext(拡張子)
    #print('base:',base)
    #print('ext:',ext)
    if ext == '.wav':
        filelists.append([file, os.path.getctime(path)])  #もしwavファイルが有ったら、作成日時を取得しリストに入れる
filelists.sort(key=itemgetter(1), reverse=True)  #リストを並び替える
MAX_CNT = 3  #残したいファイル数を指定する

for i,file in enumerate(filelists):  #変数iにインデックス(番号)、変数fileに要素を取り出す(enumerate関数)
    #print("インデックスi",i)
    #print("要素file",file)
    if i > MAX_CNT - 1:
        os.remove(path + file[0])  #ファイル削除 #変数fileは[ファイル名,作成日時]で出力。そのためファイルを削除したいためfile[0]を挿入する
    print('削除' + str(i) + '. ' + file[0])
    #print(str(i) + '. ' + file[0] + '\r\n')
#print('{}は削除します'.format(filelists))
t01 = time.time()
print('timecount',t01-t00)






#from operator import itemgetter  #リストの並び替えるライブラリ
#filelists.sort(key=itemgetter(1), reverse=True)  #リストを並び替える
#MAX_CNT = 0  #残したいファイル数を指定する
#for i,file in enumerate(filelists):
    #if i > MAX_CNT - 1:
    #    os.remove(path + file[0])
