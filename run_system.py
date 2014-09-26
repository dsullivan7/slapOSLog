import pandas as p
import numpy as np
from os import walk
from os.path import join
import matplotlib.pyplot as plt
from matplotlib import dates
import time
from datetime import datetime

datadirs = ["./softinst54228.host.vifib.net/"
            "ycdqkrovgxpfsiahwvqerhltugiznofp/",
            "./softinst54226.host.vifib.net/"
            "iyhmtkvqnoudlafpeubyfxjsqwodlcna/",
            "./softinst54243.host.vifib.net/"
            "jlauxpctiqnksohyhzsqbvgpufnoxdmr/",
            "./softinst54237.host.vifib.net/"
            "jyaophnvqtrxscugqglmrkeofwviupdj/"]
log = "server-log/"
col_index = 1
types = ["histogram", "hour_averages"]
type = types[0]

def main(index):
    mypath = datadirs[index] + log
    num = 24
    if __name__ == "__main__":
        all_column = np.array([])
        avgs = np.empty((0, num))
        for (dirpath, dirnames, filenames) in walk(mypath):
            for directory in dirnames:
                traindata = p.read_csv(join(
                    mypath, directory, "dump_system.csv"))
                stat = np.array(traindata)[:, col_index]
                if type == "hour_averages":
                    avg = np.zeros(num)
                    traindata = np.array(traindata)
                    times = traindata[:, -2]
                    times = np.array([i.split(":")[0] for i in times])
                    for i in range(num):
                        stat_hour = stat[times == str(i).zfill(2)]
                        if stat_hour.size != 0:
                            avg[i] = np.mean(stat_hour)

                    avgs = np.append(avgs, avg.reshape(1, -1), axis=0)
                elif type == "histogram":
                    all_column = np.append(all_column, stat)

        if type == "hour_averages":
            plt.plot(np.mean(avgs, axis=0))
        elif type == "histogram":
            plt.hist(all_column)

        plt.show()

if __name__ == "__main__":
    for i in range(4):
        main(i)

