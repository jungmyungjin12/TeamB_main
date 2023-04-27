import os
import xml.etree.ElementTree as elemTree
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

# 변수 설정
I = np.array([])
V = np.array([])
WL = np.array([])
WL_ref = np.array([])
TR = np.array([])
TR_ref = np.array([])
data_length_TR = np.array([])
Lot = np.array([])
row = np.array([])
column = np.array([])
Operator = np.array([])
Script_id = np.array([])
Name = np.array([])
Wafer_name = np.array([])
Mask_name = np.array([])
TestSite = np.array([])
Operator = np.array([])
Date = np.array([])
Analysis_WL = np.array([])
Max_TR_ref = np.array([])
DC_bias=[]  # 수정 필요 부분
data_WL_length = 0
data_I_length = 0
temp1 = 0
temp2 = 0
temp3 = 0

# data_file 하위 폴더에 존재하는 모든 xml 파일 이름 추출
dir_path='data_file'
file_names = [file for file in os.listdir(dir_path) if file.endswith('.xml')]
# 모든 data_file에 대하여 data parsing 진행
for file_name in file_names:
    tree = elemTree.parse(f'data_file/{file_name}')
    root = tree.getroot()
# 전류, 전압 데이터 추출
    for current in root.iter('Current'):
        I = np.append(I, abs(np.array(list(map(float, current.text.split(','))))))
    for voltage in root.iter('Voltage'):
        V = np.append(V, list(map(float, voltage.text.split(','))))
        data_I_length = np.array(list(map(float, voltage.text.split(',')))).size
    for MD in root.iter('Modulator'):
        if temp1 == 0:
            Name = np.append(Name, [MD.find('DeviceInfo').attrib['Name']])
# WL, TR, DC bias 데이터 추출
        for WL_sweep in MD.iter('WavelengthSweep'):
            if temp1 == 1:
                WL_ref = np.append(WL_ref, np.array(list(map(float, WL_sweep.find('L').text.split(',')))))
                TR_ref = np.append(TR_ref, np.array(list(map(float, WL_sweep.find('IL').text.split(',')))))
                Max_TR_ref = np.append(Max_TR_ref,[max(TR_ref)])
                data_WL_length = np.array(list(map(float, WL_sweep.find('L').text.split(',')))).size
                continue
            WL = np.append(WL, np.array(list(map(float, WL_sweep.find('L').text.split(',')))))
            TR = np.append(TR, np.array(list(map(float, WL_sweep.find('IL').text.split(',')))))
            DC_bias.append(WL_sweep.attrib['DCBias'])
        temp1+=1
# TestSiteInfo에서 구할 수 있는 데이터 추출
    for i in root.iter('TestSiteInfo'):
        Lot = np.append(Lot,[i.attrib['Batch']])
        Wafer_name = np.append(Wafer_name,[i.attrib['Wafer']])
        Mask_name = np.append(Mask_name,[i.attrib['Maskset']])
        TestSite = np.append(TestSite,[i.attrib['TestSite']])
        column = np.append(column,[i.attrib['DieColumn']])
        row = np.append(row,[i.attrib['DieRow']])
# Analysis_WL 데이터 추출
    for i in root.iter('DesignParameters'):
        if temp2 == 0:
            for k in i.iter('DesignParameter'):
                if temp3 == 1:
                    Analysis_WL = np.append(Analysis_WL,[k.text])
                temp3 += 1
        temp2 += 1
# 날짜 data 추출
    for i in root.iter('OIOMeasurement'):
        date_str = i.attrib['CreationDate']
        dt = datetime.strptime(date_str,'%a %b %d %H:%M:%S %Y')
        Date = np.append(Date, dt.strftime('%Y%m%d-%H%M%S'))
        Operator = np.append(Operator, i.attrib['Operator'])
# 적절한 shape으로 데이터 행렬 변환
I = I.reshape(len(file_names),data_I_length)
V = V.reshape(len(file_names),data_I_length)
WL = WL.reshape(len(file_names), int(WL.size/WL_ref.size), data_WL_length)
TR = TR.reshape(len(file_names), int(WL.size/WL_ref.size), data_WL_length)
WL_ref = WL_ref.reshape(len(file_names), data_WL_length)
TR_ref = TR_ref.reshape(len(file_names), data_WL_length)
I_n_1V = I[:,np.where(V == -1)[1][0]] # 1V에 대한 열 데이터 전체를 가져온 변수
I_p_1V = I[:,np.where(V == 1)[1][0]]
Max_TR_ref = Max_TR_ref.reshape(len(file_names),1)
Lot = Lot.reshape(len(file_names),1)
Wafer_name = Wafer_name.reshape(len(file_names),1)
Analysis_WL = Analysis_WL.reshape(len(file_names),1)
TestSite = TestSite.reshape(len(file_names),1)
Name = Name.reshape(len(file_names),1)
Date = Date.reshape(len(file_names),1)
Mask_name = Mask_name.reshape(len(file_names),1)
Operator = Operator.reshape(len(file_names),1)
Script_id = np.array(list('process '+row[0][-4:-1] for row in TestSite))
row = row.reshape(len(file_names),1)
column = column.reshape(len(file_names),1)
