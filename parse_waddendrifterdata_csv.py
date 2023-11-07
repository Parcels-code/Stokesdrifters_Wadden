from glob import glob
import pandas as pd
import json

directory = '2023-*'
filenames = sorted(glob(directory + '/*.csv'))

drifternames = {
    '300434068072450': 'Orka',
    '300434068077530': 'Bultrug',
    '300434068078480': 'Papegaaiduiker',
    '300434068079510': 'Beluga',
    '300434069406260': 'Henk Janssen',
    '300434068072430': 'Koen',
    '300434068070540': 'Paerdemarct',
    '300434068074490': 'Jan Loman',
    '300434068075450': '09',
    '300434068076530': '10',
    '300434068070510': '11',
    '300434069405400': '12',
    '300434069605630': '13',
    '300434066486520': '14',
    '300434069402400': '15',
    '300434068075440': '16',
    '300434068073450': '17',
    '300434068079520': '18',
    '300434068078520': '19',
    '300434068073510': '20',
    '300434068070520': '21',
    '300434068075490': '22',
    '300434068072500': '23',
    '300434068076480': '24',
}

drifterstartdates ={
    'Orka': '2023-10-06 00:00:00',
    'Bultrug': '2023-10-06 00:00:00',
    'Papegaaiduiker': '2023-10-06 00:00:00',
    'Beluga': '2023-10-06 00:00:00',
    'Henk Janssen': '2023-10-06 00:00:00',
    'Koen': '2023-10-06 00:00:00',
    'Paerdemarct': '2023-10-06 00:00:00',
    'Jan Loman': '2023-10-06 00:00:00',
    '09': '2023-10-06 00:00:00',
    '10': '2023-10-06 00:00:00',
    '11': '2023-10-06 00:00:00',
    '12': '2023-10-06 00:00:00',
    '13': '2023-10-06 00:00:00',
    '14': '2023-10-06 00:00:00',
    '15': '2023-10-06 00:00:00',
    '16': '2023-10-06 00:00:00',
    '17': '2023-10-06 00:00:00',
    '18': '2023-10-06 00:00:00',
    '19': '2023-10-06 00:00:00',
    '20': '2023-10-06 00:00:00',
    '21': '2023-10-06 00:00:00',
    '22': '2023-10-06 00:00:00',
    '23': '2023-10-06 00:00:00',
    '24': '2023-10-06 00:00:00',
}

df = pd.concat((pd.read_csv(f) for f in filenames), ignore_index=True)
df['Name'] = [drifternames[f.split('/')[-1].split('_')[0]] for f in filenames]
df['Orientation'] = df['Hex Data'].str.split('orientation=').str[1].str.split(';').str[0].astype(int)
df['Voltage'] = df['Hex Data'].str.split('voltage=').str[1].str.split(';').str[0].astype(float)
df.sort_values(by=['Name', 'Data Date(GMT)'], inplace=True)#.drop('Hex Data', axis=1)

waddendata = {}
for i in df['Name'].unique():
    dfi = df[df['Name'] == i][['Data Date(GMT)', 'LATITUDE', 'LONGITUDE', 'Orientation', 'Voltage']]
    dfi = dfi[dfi['Data Date(GMT)'] > drifterstartdates[i]]
    waddendata[i] = list(dfi.itertuples(index=False, name=None))

with open('waddendrifters_roof.json', 'w') as filejson:
    json.dump(waddendata, filejson)

print("Done parsing data")
