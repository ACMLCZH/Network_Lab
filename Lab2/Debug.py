import numpy as np
import time


def info1(transfer):
    fw = open(f"./log/log_{time.time()}.txt", "w")
    print(transfer.aud_list_vol, file=fw)
    for i in range(len(transfer.txt_list)):
        lowd, highd = transfer.seg_list[i]
        print(i, transfer.seg_list[i], transfer.txt_list[i],
              np.max(transfer.aud_list_vol[lowd: highd]), np.min(transfer.aud_list_vol[lowd: highd]),
              transfer.aud_list_vol[highd - 6: highd],
              file=fw)
    fw.close()
