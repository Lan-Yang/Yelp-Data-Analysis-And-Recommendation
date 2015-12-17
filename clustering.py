# file that do recommendation

import pickle
from pyspark import SparkContext
from pyspark.mllib.recommendation import ALS, MatrixFactorizationModel, Rating

rating_tuple_list = pickle.load(open('rating_tuple_pickle', 'rb'))

sc = SparkContext()

# trian the model
ratings = sc.parallelize(rating_tuple_list)
model = ALS.train(ratings, 5, seed=10)



user_dict = pickle.load(open('res_user_inddict_pickle', 'rb'))

user_inds = user_dict.values()
user_recom_list = []

for user_i in user_inds:
	rec_list = model.recommendProducts(user_i, 5)
	user_recom_list.append(rec_list)


pickle.dump(user_recom_list, open('user_recom_list_pickle', 'wb'))
