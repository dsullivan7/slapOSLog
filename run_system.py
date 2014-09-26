import pandas as p
import numpy as np
import pdb
from os import walk
from os.path import join
import matplotlib.pyplot as plt
from matplotlib import dates
import time
from datetime import datetime

datadirs = ["softinst54228.host.vifib.net/"
            "ycdqkrovgxpfsiahwvqerhltugiznofp/",
            "softinst54226.host.vifib.net/"
            "iyhmtkvqnoudlafpeubyfxjsqwodlcna/",
            "softinst54243.host.vifib.net/"
            "jlauxpctiqnksohyhzsqbvgpufnoxdmr/",
            "softinst54237.host.vifib.net/"
            "jyaophnvqtrxscugqglmrkeofwviupdj/"]
log = "server-log/"
col_index = 1
perc = .04
top = 2
types = ["histogram", "hour_averages", "topperc", "maxes"]
type = types[0]


def main(index):
    mypath = datadirs[index] + log
    num = 24
    if __name__ == "__main__":
        all_column = np.array([])
        maxes = []
        topperc = np.empty((0, 2))
        avgs = np.empty((0, num))
        dates = []
        for (dirpath, dirnames, filenames) in walk(mypath):
            for directory in dirnames:
                traindata = p.read_csv(join(
                    mypath, directory, "dump_system.csv"))
                traindata = np.array(traindata)
                dates.append(directory)
                stat = np.array(traindata)[:, col_index]
                if type == "hour_averages":
                    avg = np.zeros(num)
                    times = traindata[:, -2]
                    times = np.array([i.split(":")[0] for i in times])
                    for i in range(num):
                        stat_hour = stat[times == str(i).zfill(2)]
                        if stat_hour.size != 0:
                            avg[i] = np.mean(stat_hour)

                    avgs = np.append(avgs, avg.reshape(1, -1), axis=0)
                elif type == "histogram":
                    all_column = np.append(all_column, stat)

                elif type == "topperc":
                    topperc = np.append(topperc,
                                        traindata[:, [col_index, -2]], axis=0)
                elif type == "maxes":
                    maxes.append(np.max(stat))
                    avg = np.zeros(num)
                    times = traindata[:, -2]
                    times = np.array([i.split(":")[0] for i in times])
                    for i in range(num):
                        stat_hour = stat[times == str(i).zfill(2)]
                        if stat_hour.size != 0:
                            avg[i] = np.mean(stat_hour)

                    avgs = np.append(avgs, avg.reshape(1, -1), axis=0)

        if type == "hour_averages":
            plt.plot(np.mean(avgs, axis=0))
            plt.title(datadirs[index].split(".")[0] + " average cpu% by hour")
            plt.xlabel("hour")
            plt.ylabel("cpu %")
            plt.plot(avgs[i])
            plt.show()
            plt.show()
        elif type == "histogram":
            plt.title(datadirs[index].split(".")[0] + " cpu% histogram")
            plt.xlabel("cpu%")
            plt.ylabel("frequency")
            plt.hist(all_column)
            plt.show()
        elif type == "topperc":
            mi = np.argsort(topperc[:, 0])
            mi = mi[: -mi.size * perc]
            topperc = topperc[mi]
            topperc[:, 1] = np.array([int(i.split(":")[0]) for i in topperc[:, 1]])
            plt.hist(topperc[:, 1], bins=24)
            plt.show()
        elif type == "maxes":
            mi = np.argsort(maxes)
            mi = mi[-top:]
            for i in mi:
                plt.title(datadirs[index].split(".")[0] + "\n"
                          + dates[i])
                plt.xlabel("hour")
                plt.ylabel("cpu %")
                plt.plot(avgs[i])
                plt.show()

if __name__ == "__main__":
    for i in range(4):
        main(i)

