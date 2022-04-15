import pandas as pd
import os
import cv2
import random
from textblob import TextBlob
from plotly.offline import iplot
# import plotly.graph_objs as go
# import plotly.plotly as py
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns



import cufflinks as cf
cf.go_offline()
cf.set_config_file(offline=False, world_readable=True)
df = pd.read_csv('new1.csv',encoding= 'utf-8')
def preprocess(ReviewText):
    ReviewText = ReviewText.str.replace("(<br/>)", "")
    ReviewText = ReviewText.str.replace('(<a).*(>).*(</a>)', '')
    ReviewText = ReviewText.str.replace('(&amp)', '')
    ReviewText = ReviewText.str.replace('(&gt)', '')
    ReviewText = ReviewText.str.replace('(&lt)', '')
    ReviewText = ReviewText.str.replace('(\xa0)', ' ')
    return ReviewText
df['Reviews'] = preprocess(df['Reviews'])


df['polarity'] = df['Reviews'].map(lambda text: TextBlob(text).sentiment.polarity)
df['review_len'] = df['Reviews'].astype(str).apply(len)
df['word_count'] = df['Reviews'].apply(lambda x: len(str(x).split()))


# print(min(df.polarity))
# print('5 random reviews with the highest positive sentiment polarity: \n')
# cl = df.loc[df.polarity == 1, ['Reviews']].sample(5).values
# for c in cl:
#     print(c[0])

# print('2 reviews with the most negative polarity: \n')
# cl = df.loc[df.polarity == -1.0, ['Reviews']].sample(2).values
# for c in cl:
#     print(c[0])

# df['polarity'].plot.bar()
# df.groupby('Category').count()['Restaurant ID'].sort_values(ascending=False)

# df.groupby('Category').count()['Restaurant ID'].sort_values(ascending=True).plot.bar()
df['Category'].value_counts()[[1,2,3,4,5]].plot(kind = 'bar')
plt.xlabel('Category')
plt.ylabel('Restaurants')
plt.show()


print('done')
