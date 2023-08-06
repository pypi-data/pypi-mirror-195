"""
牧德原始数据的查找整理。
原始牧德文件包含Project、Defect和VerifyResult三个文件夹，没问文件由project、layer、date组成，此.py用于查找三个文件夹的交集并记录成.ini
"""

import os
import shutil
import config  # 载入设置文件

WIDTH = 108
HEIGHT = 108
RESOLUTION = 12.5
DIGIT = 64
digit = 6

PATH = config.PATH
Data_Path = config.setting['NetworkSetting']['DataPath']
Defect_Path = config.setting['NetworkSetting']['DefectPath']
Project_Path = config.setting['NetworkSetting']['ProjectPath']
VerifyResult_path = config.setting['NetworkSetting']['VRSVerifyPath']
NewVerifyResult_path = config.setting['NetworkSetting']['NewVerifyResultpath']

