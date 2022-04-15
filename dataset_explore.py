import pandas as pd
import os
import cv2
import random
review_data = pd.read_csv('new2.csv',encoding= 'utf-8')
# res_name = list((set(review_data['Restaurant Name'])))

# for n,res in zip(list(os.listdir('images')),res_name):
#     n = os.path.join('images',n)
#     temp = res + '.png'
#     temp = os.path.join('images',temp)
#     os.rename(n,temp)


def get_data_single(res):
    global review_data
    hdict = {}
    res = res
    hdict['Reviews'] = "Lol1"
    hotel_subset = review_data[review_data['Restaurant Name'] == res]
    hdict['Restaurant ID'] = list(hotel_subset['Restaurant ID'])[0]
    hdict['Restaurant Name'] = res
    hdict['Address'] = list(hotel_subset['Address'])[0]
    hdict['Cuisines'] = list(hotel_subset['Cuisines'])[0]
    hdict['Average Cost for two'] = list(hotel_subset['Average Cost for two'])[0]
    hdict['Has Table booking'] = list(hotel_subset['Has Table booking'])[0]
    hdict['Has Online delivery'] = list(hotel_subset['Has Online delivery'])[0]
    hdict['Aggregate rating'] = list(hotel_subset['Aggregate rating'])[0]
    hdict['Rating text'] = list(hotel_subset['Rating text'])[0]
    hdict['Votes'] = list(hotel_subset['Votes'])[0]
    hdict['Category'] = list(hotel_subset['Category'])[0]
    hdict['User_email'] = 'lol1'
    review_data = review_data.append(hdict, ignore_index = True)
    review_data.to_csv('new2.csv', index = False)


get_data_single("Balay Dako")

# for i in range(len(data['Reviews'])):
#     print(data['Reviews'][i])
#     print(data['User_email'][i])













# review_data = review_data.dropna()
# review_data = review_data.drop(['url','online_order','book_table','votes','menu_item'],axis = 1)
# hotels = list(set(list(review_data['name'])))
# fin = hotels[100:150]
# bool = review_data['name'].isin(fin)
# review_data1 = review_data[bool]
# review_data = review_data[pd.to_numeric(review_data['id'], errors='coerce').notnull()]
# review_data = review_data.dropna()
# review_data.to_csv('new3.csv')

#

# print(len(data))
# fin = []
# for h in hello:
#     if len(h) == 2:
#         fin.append(h)
#
# fin = fin[11:16]
# print(len(set(review_data1['name'])))

# review_data1.to_csv('new.csv')
