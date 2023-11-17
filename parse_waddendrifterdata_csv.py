from glob import glob
import pandas as pd
import json

directory = '/science/wwwprojects/plasticadrift/www/galapagosdrifters/202*'
filenames = sorted(glob(directory + '/*.csv'))

drifterinfo = {
    '300434068072450': (1, 'Orka', '2023-11-14 10:21:12',4,55.507,52,56.821),
    '300434068077530': (2, 'Bultrug', '2023-11-14 10:21:36',4,55.526,52,56.808),
    '300434068078480': (3, 'Papegaaiduiker', '2023-11-14 10:22:38',4,55.531,52,56.819),
    '300434068079510': (4, 'Splinter', '2023-11-14 13:01:34',4,57.263,53,01.244),
    '300434069406260': (5, 'Henk Janssen', '2023-11-14 13:02:34',4,57.292,53,01.247),
    '300434068072430': (6, 'Koen', '2023-11-14 13:53:04',4,56.768,53,06.721),
    '300434068070540': (7, 'Paerdemarct', '2023-11-14 10:24:30',4,55.604,52,56.698),
    '300434068074490': (8, 'Jan Loman', '2023-11-14 10:25:05',4,55.609,52,56.710),
    '300434068075450': (9, 'Pizza Funghi', '2023-11-14 10:25:41',4,55.594,52,56.712),
    '300434068076530': (10, 'Pizza Margherita', '2023-11-14 12:57:00',4,57.168,53,01.139),
    '300434068070510': (11, 'Pizza Quatro Formagio', '2023-11-14 12:58:17',4,57.188,53,01.140),
    '300434069405400': (12, 'Pizza Napolitana', '2023-11-14 12:59:50',4,57.181,53,01.153),
    '300434069605630': (13, 'Pizza Verdura', '2023-11-14 10:27:27',4,55.738,52,56.820),
    '300434066486520': (14, 'Pizza Vegetariana', '2023-11-14 10:27:44',4,55.710,52,56.821),
    '300434069402400': (15, 'Pizza Calzone', '2023-11-14 10:28:29',4,55.723,52,56.814),
    '300434068075440': (16, 'Pizza Quatro Stagione', '2023-11-14 13:53:51',4,56.782,53,06.723),
    '300434068073450': (17, 'Pizza Caprese', '2023-11-14 13:03:00',4,57.275,53,01.255),
    '300434068079520': (18, 'Michelangelo', '2023-11-14 13:04:32',4,57.379,53,01.147),
    '300434068078520': (19, 'Rafael', '2023-11-14 13:54:29',4,56.784,53,06.711),
    '300434068073510': (20, 'Donatello', '2023-11-14 13:04:59',4,57.390,53,01.136),
    '300434068070520': (21, 'Leonardo', '2023-11-14 13:49:23',4,57.011,53,06.713),
    '300434068075490': (22, 'Beluga', '2023-11-14 13:06:00',4,57.369,53,01.139),
    '300434068072500': (23, 'Babette', '2023-11-14 13:49:48',4,57.025,53,06.720),
    '300434068076480': (24, 'Ciaran', '2023-11-14 13:50:25',4,57.010,53,06.728),
}

print(f"Number of files: {len(filenames)}")
df = pd.concat((pd.read_csv(f) for f in filenames), ignore_index=True)
print('Done loading csv files')

df['Name'] = [drifterinfo[f.split('/')[-1].split('_')[0]][1] for f in filenames]
df['Orientation'] = df['Hex Data'].str.split('orientation=').str[1].str.split(';').str[0].astype(int)
df['Voltage'] = df['Hex Data'].str.split('voltage=').str[1].str.split(';').str[0].astype(float)
df['FixValid'] = df['Hex Data'].str.split('fixValid=').str[1].str.split(';').str[0].astype(bool)
df['TimetoFix'] = df['Hex Data'].str.split('timeToFix=').str[1].str.split(';').str[0].astype(int)
df['FixTime'] = df['Hex Data'].str.split('fixTime=').str[1].str.split(';').str[0].astype(int)
df['SST'] = df['Hex Data'].str.split('temperature=').str[1].astype(float)

df = df[df['LONGITUDE'] < 175]  # Removing Outliers

df.sort_values(by=['Name', 'Data Date(GMT)'], inplace=True)

vars = [['Data Date(GMT)', 'LATITUDE', 'LONGITUDE'],
        ['Data Date(GMT)', 'LATITUDE', 'LONGITUDE', 'Orientation', 'Voltage', 'FixValid', 'TimetoFix', 'FixTime', 'SST']]
fnames = ['/science/wwwprojects/plasticadrift/www/galapagosdrifters/waddendrifters.json',
          '/science/wwwprojects/plasticadrift/www/galapagosdrifters/waddendrifters_detailed.json']
for detailed in [0, 1]:
    waddendata = {}
    for i in dict(sorted(drifterinfo.items(), key=lambda item: item[1][2])):
        name = drifterinfo[i][1]
        dfi = df[df['Name'] == name][vars[detailed]]
        dfi = dfi[dfi['Data Date(GMT)'] > drifterinfo[i][2]]
        if detailed == 0:  # remove points with sudden large change in lon/lat for website version only
            dfi = dfi[abs(dfi['LATITUDE'].diff()) < 0.05]
            dfi = dfi[abs(dfi['LONGITUDE'].diff()) < 0.05]
        waddendata[name] = list(dfi.itertuples(index=False, name=None))
        if len(waddendata[name]) > 0:
            if detailed == 0:
                waddendata[name].insert(0, (drifterinfo[i][2], round(drifterinfo[i][5]+drifterinfo[i][6]/60,5), round(drifterinfo[i][3]+drifterinfo[i][4]/60,5)))
            if detailed == 1:
                waddendata[name].insert(0, (drifterinfo[i][2], round(drifterinfo[i][5]+drifterinfo[i][6]/60,5), round(drifterinfo[i][3]+drifterinfo[i][4]/60,5),
                                            waddendata[name][0][3], waddendata[name][0][4], waddendata[name][0][5], waddendata[name][0][6], waddendata[name][0][7], waddendata[name][0][8]))

        if detailed == 1:
            print(name, len(waddendata[name]))

    with open(fnames[detailed], 'w') as filejson:
        json.dump(waddendata, filejson)

print("Done parsing data")
