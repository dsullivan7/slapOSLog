from os import walk
from os.path import join
import pandas as p
import numpy as np

datadirs = [("softinst54228.host.vifib.net",
            "ycdqkrovgxpfsiahwvqerhltugiznofp"),
            ("softinst54226.host.vifib.net",
             "iyhmtkvqnoudlafpeubyfxjsqwodlcna"),
            ("softinst54243.host.vifib.net",
             "jlauxpctiqnksohyhzsqbvgpufnoxdmr"),
            ("softinst54237.host.vifib.net",
             "jyaophnvqtrxscugqglmrkeofwviupdj")]
log = "server-log"

times = []
for i in range(24):
    for j in range(1, 60):
        times.append(str(i).zfill(2) + str(j).zfill(2))


def main():
    not_logged = []
    for server, h in datadirs:
        for (dirpath, dirnames, filenames) in walk(join(server, h, log)):
            for directory in dirnames:
                log_times = []
                traindata = p.read_csv(join(server, h, log,
                                            directory, "dump_system.csv"))
                traindata = np.array(traindata)
                day_times = traindata[:, -2]

                for t in day_times:
                    concat = "".join(t.split(":")[:2])
                    log_times.append(concat)

                logging = True
                for t in times:
                    if t not in log_times and logging:
                        start = t
                        counter = 1
                        logging = False
                    elif t in log_times and not logging:
                        if counter > 1:
                            not_logged.append((server, directory, start, t))
                        logging = True
                    else:
                        counter += 1

    for i in not_logged:
        print(i)


if __name__ == "__main__":
    main()
