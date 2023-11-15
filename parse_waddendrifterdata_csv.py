from glob import glob
import pandas as pd
import json

directory = '2023-*'
filenames = sorted(glob(directory + '/*.csv'))

drifternames = {
    '300434068072450': 'Orka',
    '300434068077530': 'Bultrug',
    '300434068078480': 'Papegaaiduiker',
    '300434068079510': 'Splinter',
    '300434069406260': 'Henk Janssen',
    '300434068072430': 'Koen',
    '300434068070540': 'Paerdemarct',
    '300434068074490': 'Jan Loman',
    '300434068075450': 'Pizza Funghi',
    '300434068076530': 'Pizza Margherita',
    '300434068070510': 'Pizza Quatro Formagio',
    '300434069405400': 'Pizza Napolitana',
    '300434069605630': 'Pizza Verdura',
    '300434066486520': 'Pizza Vegetariana',
    '300434069402400': 'Pizza Calzone',
    '300434068075440': 'Pizza Quatro Stagione',
    '300434068073450': 'Pizza Caprese',
    '300434068079520': 'Michelangelo',
    '300434068078520': 'Rafael',
    '300434068073510': 'Donatello',
    '300434068070520': 'Leonardo',
    '300434068075490': 'Beluga',
    '300434068072500': 'Babette',
    '300434068076480': 'Ciaran',
}

drifterstartdates ={
    'Orka': '2023-11-14 10:21:12',
    'Bultrug': '2023-11-14 10:21:36',
    'Papegaaiduiker': '2023-11-14 10:22:38',
    'Splinter': '2023-11-14 13:01:34',
    'Henk Janssen': '2023-11-14 13:02:34',
    'Koen': '2023-11-14 13:53:04',
    'Paerdemarct': '2023-11-14 10:24:30',
    'Jan Loman': '2023-11-14 10:25:05',
    'Pizza Funghi': '2023-11-14 10:25:41',
    'Pizza Margherita': '2023-11-14 12:57:00',
    'Pizza Quatro Formagio': '2023-11-14 12:58:17',
    'Pizza Napolitana': '2023-11-14 12:59:50',
    'Pizza Verdura': '2023-11-14 10:27:27',
    'Pizza Vegetariana': '2023-11-14 10:27:44',
    'Pizza Calzone': '2023-11-14 10:28:29',
    'Pizza Quatro Stagione': '2023-11-14 13:53:51',
    'Pizza Caprese': '2023-11-14 13:03:00',
    'Michelangelo': '2023-11-14 13:04:32',
    'Rafael': '2023-11-14 13:54:29',
    'Donatello': '2023-11-14 13:04:59',
    'Leonardo': '2023-11-14 13:49:23',
    'Beluga': '2023-11-14 13:06:00',
    'Babette': '2023-11-14 13:49:48',
    'Ciaran': '2023-11-14 13:50:25',
}

df = pd.concat((pd.read_csv(f) for f in filenames), ignore_index=True)
df['Name'] = [drifternames[f.split('/')[-1].split('_')[0]] for f in filenames]
df['Orientation'] = df['Hex Data'].str.split('orientation=').str[1].str.split(';').str[0].astype(int)
df['Voltage'] = df['Hex Data'].str.split('voltage=').str[1].str.split(';').str[0].astype(float)
df['FixValid'] = df['Hex Data'].str.split('fixValid=').str[1].str.split(';').str[0].astype(bool)
df['TimetoFix'] = df['Hex Data'].str.split('timeToFix=').str[1].str.split(';').str[0].astype(int)
df['FixTime'] = df['Hex Data'].str.split('fixTime=').str[1].str.split(';').str[0].astype(int)
df['SST'] = df['Hex Data'].str.split('temperature=').str[1].astype(float)

df.sort_values(by=['Name', 'Data Date(GMT)'], inplace=True)#.drop('Hex Data', axis=1)

waddendata = {}
for i in dict(sorted(drifterstartdates.items(), key=lambda item: item[1])):
    dfi = df[df['Name'] == i][['Data Date(GMT)', 'LATITUDE', 'LONGITUDE', 'Orientation', 'Voltage', 'FixValid', 'TimetoFix', 'FixTime', 'SST']]
    dfi = dfi[dfi['Data Date(GMT)'] > drifterstartdates[i]]
    dfi = dfi[dfi['LONGITUDE'] < 175]
    waddendata[i] = list(dfi.itertuples(index=False, name=None))
    print(i, len(waddendata[i]))

with open('waddendrifters.json', 'w') as filejson:
    json.dump(waddendata, filejson)

print("Done parsing data")
