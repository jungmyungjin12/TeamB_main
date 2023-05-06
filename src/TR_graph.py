# 라이브러리 import
with open('library.txt','r') as f:
    for library in f:
        exec(library)
import functions as fc
warnings.filterwarnings('ignore',category=np.RankWarning)
def plot_TR_graph(Wafer,Date,Position):

    wave_len = np.array([])
    wave_len_ref = np.array([])
    trans = np.array([])
    wave_len_half = []
    trans_half = []
    trans_ref = np.array([])
    wave_len_half = np.array([])
    trans_half = np.array([])
    wave_len_max = np.array([])
    trans_max = np.array([])
    smoothed_trans = np.array([])
    temp1 = 0
    temp2 = 0

    path = os.path.join('..','dat',Wafer,Date)
    file_name = [os.path.join(path,f) for f in os.listdir(path) if 'LMZ' in f and f.endswith('.xml') and Position in f]

    tree = elemTree.parse(file_name[0])
    root = tree.getroot()

    for modulator in root.iter('Modulator'):
        for WL_sweep in modulator.iter('WavelengthSweep'):
            if temp1 == 1:
                wave_len_ref = np.append(wave_len_ref, np.array(list(map(float, WL_sweep.find('L').text.split(',')))))
                trans_ref = np.append(trans_ref, np.array(list(map(float, WL_sweep.find('IL').text.split(',')))))
                continue
            wave_len = np.append(wave_len, np.array(list(map(float, WL_sweep.find('L').text.split(',')))))
            trans = np.append(trans, np.array(list(map(float, WL_sweep.find('IL').text.split(',')))))
            temp2 += 1
        temp1 += 1
    wave_len = wave_len.reshape(temp2,int(trans.size/temp2))
    trans = trans.reshape(temp2,int(trans.size/temp2))
    fit_trans_ref = fc.Ref_fitted_data(wave_len_ref,trans_ref)
    s = 150
    for i in range(wave_len.shape[0]):
    # for i in range(1,2):
        trans[i] = trans[i] - fit_trans_ref
        for k in range(wave_len.shape[1]):
            count = 0
            if k >= (wave_len.shape[1]-(s+1)):
                continue
            for g in range(1,(s+1)):
                if trans[i][k] > trans[i][k+g]:
                    count += 1
            if count >= s-4:
                trans_half.append(trans[i][k])
                wave_len_half.append(wave_len[i][k])
                
    for i in range(wave_len_half.shape[0]):
        for j in range(wave_len_half.size):
            if j == 0:
                wave_len_max = np.append(wave_len_max, wave_len_half[i][j])
                trans_max = np.append(trans_max, trans_half[i][j])
                continue
            elif j >= wave_len_half.size - 3:
                continue
            if (wave_len_half[i][j + 2] - wave_len_half[i][j + 1]) >= (wave_len_half[i][j + 1] - wave_len_half[i][j] + 6):
                wave_len_max = np.append(wave_len_max, wave_len_half[i][j + 2])
                trans_max = np.append(trans_max, trans_half[i][j + 2])
        plt.plot(wave_len_max,trans_max,'ro')
    wave_len_max = wave_len_max.reshape(temp2, int(wave_len_max.size / temp2))
    trans_max = trans_max.reshape(temp2,int(trans_max.size / temp2))
    # 극댓값 정보를 찾기 -> 여러개 시도
    # trans_max = trans_max.reshape(wave_len.shape[0],trans_max.size/wave_len.shape[0])
    # for i in range(wave_len.shape[0]):
    #     plt.plot(wave_len[i],trans[i])
    print(wave_len_max, trans_max)
    plt.show()
plot_TR_graph('D07','20190715_190855','(0,0)')

'''  -> 시도 방법 1 (극댓값 찾기)
            for k in range(2,wave_len.shape[1]):
                if k == wave_len.shape[1]-1:
                    continue
                if trans[i][k]>trans[i][k-1] and trans[i][k]<trans[i][k+1]:
                    trans_max = np.append(trans_max,trans[i][k])
                    wave_len_max = np.append(wave_len_max,wave_len[i][k])
        print(trans_max.size,wave_len.shape[0])
        plt.plot(wave_len_max, trans_max,'ro')
'''