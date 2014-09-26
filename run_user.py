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
col_index = 6
types = ["histogram", "hour_averages"]
type = types[0]


def main(index):
    mypath = datadirs[index] + log
    num = 24
    if __name__ == "__main__":
        user_stats = {}
        for (dirpath, dirnames, filenames) in walk(mypath):
            for directory in dirnames:
                traindata = p.read_csv(join(
                    mypath, directory, "dump_user.csv"))
                traindata = np.array(traindata)
                stat = traindata[:, col_index]
                users = traindata[:, 0]
                if type == "hour_averages":
                    times = traindata[:, -2]
                    for user in np.unique(users):
                        if not user in user_stats:
                            user_stats[user] = np.empty((0, num))
                        break
                    for user in np.unique(users):
                        user_times = times[users == user]
                        user_times = np.array([i.split(":")[0] for i in times])
                        avg = np.zeros(num)
                        for i in range(num):
                            stat_hour = stat[user_times == str(i).zfill(2)]
                            if stat_hour.size != 0:
                                avg[i] = np.mean(stat_hour)

                        user_stats[user] = np.append(user_stats[user],
                                                     avg.reshape(1, -1),
                                                     axis=0)
                        break
                elif type == "histogram":
                    for user in np.unique(users):
                        if not user in user_stats:
                            user_stats[user] = np.array([])
                        break
                    for user in np.unique(users):
                        user_stats[user] = np.append(user_stats[user], stat)
                        break

        if type == "hour_averages":
            for user in user_stats:
                plt.plot(np.mean(user_stats[user], axis=0))
                plt.show()
                break
        elif type == "histogram":
            for user in user_stats:
                plt.hist(user_stats[user])
                plt.show()
                break

if __name__ == "__main__":
    for i in range(1):
        main(i)

