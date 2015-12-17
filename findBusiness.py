# file that find the intersect between business file and review file


import csv
import json
import csv,codecs,cStringIO
import pickle


# save the business id into dictionary
bus_dict = {}

rating_list = []

with codecs.open('../yelp_dataset_challenge_academic_dataset/yelp_academic_dataset_business.json','rU','utf-8') as f:

    count = 0
    for line in f:
        
        if 'Restaurants' in json.loads(line)['categories']:
            bus_dict[json.loads(line)['business_id']] = True
            
find_counter = 0
with codecs.open('../yelp_dataset_challenge_academic_dataset/yelp_academic_dataset_review.json','rU','utf-8') as f:

    count = 0
    for line in f:
        
        if json.loads(line)['business_id'] in bus_dict:
            rating_list.append([json.loads(line)['business_id'], json.loads(line)['user_id'], json.loads(line)['stars']])
            count += 1
            print count

        




pickle.dump(rating_list, open('rating_list_pickle', 'wb'))