import pickle
import csv, codecs, cStringIO
import json
from pyspark.mllib.recommendation import ALS, MatrixFactorizationModel, Rating


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




recom_list = pickle.load(open('user_recom_list_pickle', 'rb'))
user_dict = pickle.load(open('res_user_inddict_pickle', 'rb'))
bus_dict = pickle.load(open('res_bus_inddict_pickle', 'rb'))



bus_name_dict = {}
with codecs.open('../yelp_dataset_challenge_academic_dataset/yelp_academic_dataset_business.json','rU','utf-8') as f:

    for line in f:
        bus_name_dict[json.loads(line)['business_id']] = json.loads(line)['name']
        

user_counter = 0

bus_ind_dict = {}

for bus_id, bus_ind in bus_dict.iteritems():
    bus_ind_dict[bus_ind] = bus_id

print "reverse done"

data = []



for each_user in recom_list:

    user_counter += 1

    # find the user id with the index
    for user_id, user_ind in user_dict.iteritems():
        if user_ind == each_user[0].user:
            row_list = [user_id]

    for each_rec in each_user:

        row_list.append(bus_name_dict[bus_ind_dict[each_rec.product]])
        
    print user_counter

    data.append(row_list)

 
with open('recommendation.csv','w') as fp:

    writer = UnicodeWriter(fp, quoting=csv.QUOTE_ALL)
    writer.writerows(data)


