# file that give each business and user id integers


import pickle
import random

user_ind_dict = {}
business_ind_dict = {}

user_ind = 1
business_ind = 1

# read the rating list for restaurants
rating_list = pickle.load(open('rating_list_pickle', 'rb'))

sample_rating_list = random.sample(rating_list,100000)

# tuple list
rating_tuple = []

for each_rating in sample_rating_list:

	# if user not in dict, add it
	if each_rating[1] not in user_ind_dict:
		user_ind_dict[each_rating[1]] = user_ind
		user_ind += 1

	# if business not in dict, add it
	if each_rating[0] not in business_ind_dict:
		business_ind_dict[business_ind] = each_rating[0]
		business_ind += 1


	# add the tuple to the list
	rating_tuple.append((user_ind_dict[each_rating[1]], business_ind_dict[each_rating[0]], each_rating[2]))


print len(rating_tuple)
pickle.dump(user_ind_dict, open('res_user_inddict_pickle', 'wb'))
pickle.dump(business_ind_dict, open('res_bus_inddict_pickle', 'wb'))

pickle.dump(rating_tuple, open('rating_tuple_pickle', 'wb'))
