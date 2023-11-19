from glob import glob
import os.path
import pandas as pd

directory = '/science/wwwprojects/plasticadrift/www/galapagosdrifters/202*'
dirnames = sorted(glob(directory))

print("Now merging daily csv files")
for dir in dirnames[:-1]:  # Don't merge last day yet
    date = dir[-10:]
    print(dir, date)
    allfilenames = sorted(glob(f"{dir}/300*.csv"))
    imeis = set([f"300{f.split('300')[1][:12]}" for f in allfilenames])
    for imei in imeis:
        fname = f"/science/wwwprojects/plasticadrift/www/galapagosdrifters/daily_merged/{imei}_{date}.csv"
        if not os.path.isfile(fname):
            filenames = sorted(glob(f"{dir}/{imei}*.csv"))
            df = pd.concat((pd.read_csv(f) for f in filenames), ignore_index=True)
            df.to_csv(fname)
