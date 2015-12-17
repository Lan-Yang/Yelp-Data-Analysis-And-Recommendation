# file that transform JSON to csv file


import json
import csv,codecs,cStringIO
import pickle

tem_count = 0
json_data = []


class UnicodeWriter:
    def __init__(self, f, dialect=csv.excel, encoding="utf-8-sig", **kwds):
        self.queue = cStringIO.StringIO()
        self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
        self.stream = f
        self.encoder = codecs.getincrementalencoder(encoding)()
    def writerow(self, row):
        '''writerow(unicode) -> None
        This function takes a Unicode string and encodes it to the output.
        '''
        self.writer.writerow([s.encode("utf-8") for s in row])
        data = self.queue.getvalue()
        data = data.decode("utf-8")
        data = self.encoder.encode(data)
        self.stream.write(data)
        self.queue.truncate(0)

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)


with codecs.open('../yelp_dataset_challenge_academic_dataset/yelp_academic_dataset_business.json','rU','utf-8') as f:

    for line in f:
        
        json_data.append(json.loads(line))
        
        tem_count += 1

data_mat = [['id', 'name', 'category', 'state', 'city', 'stars', 'longitude', 'latitude']]

for each in json_data:

    if 'Restaurants' in each['categories']:
        if len(each['categories']) == 0:
            continue

        if 'Restaurants' == each['categories'][0] and len(each['categories']) > 1:
            data_mat.append([each['business_id'], each['name'], each['categories'][1], each['state'], each['city'], unicode(each['stars']), unicode(each['longitude']), unicode(each['latitude'])])
        
        else:
            data_mat.append([each['business_id'], each['name'], each['categories'][0], each['state'], each['city'], unicode(each['stars']), unicode(each['longitude']), unicode(each['latitude'])])




'''for each in data_mat:
    for each_item in each:
        if u'\xe9' in each_item:
            print each'''
        #



with open('business.csv','w') as fp:

    writer = UnicodeWriter(fp, quoting=csv.QUOTE_ALL)
    data = data_mat

    writer.writerows(data)



