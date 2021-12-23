#coding:utf-8
"""
ファイル解凍
"""
import zipfile
import paramiko
from datetime import datetime  #タイムスタンプを実行するライブラリ
import os  #ファイルやディレクトリをパス操作するライブラリ
import shutil  #ファイル、ディレクトリの移動、コピーするライブラリ
import glob  #複数のファイルを選択するライブラリ
from natsort import natsorted  #数字の順番に並べ替えるライブラリ（自然順アルゴリズム）

#パス先
path = "/home/pi/Documents/"  #ディレクトリ先を変数pathに格納(データの格納先デレクトリを読み出すときに使用する)
File_List = glob.glob(path + "*.zip")

for extractedfile in natsorted(File_List):
    with zipfile.ZipFile(extractedfile) as unzf:
        unzf.extractall(path)

print("finish")
