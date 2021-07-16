
# In[1]:


import pandas as pd
import nltk


# In[11]:


df = pd.read_csv('/FIPS_tone_sklearn_.csv')
df


# In[12]:


nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer
sid = SentimentIntensityAnalyzer()


# In[13]:


nltk.download('punkt')


# In[14]:

# Test it 
sid.polarity_scores('I love you!')


# In[21]:


def dict_converter(dict1):
    dictlist = list()
    for key, value in dict1.items():
        temp = [key,value]
        dictlist.append(temp)
    return dictlist

dict_converter({'neg': 0.0, 'neu': 1.0, 'pos': 0.0, 'compound': 0.0})


# In[22]:


tweets = list()
for _ in df['text']:
    dict_res = dict_converter(sid.polarity_scores(_))
    #nltk.sentiment.util.demo_vader_instance(_)
    tweets.append([_, dict_res[0][1], dict_res[1][1], dict_res[2][1], dict_res[3][1]])

tweets = pd.DataFrame(tweets)
tweets.columns = ['text', 'neg', 'neu', 'pos', 'compound']
tweets

