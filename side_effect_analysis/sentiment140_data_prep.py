import numpy as np
import pandas as pd
import re
from sklearn.model_selection import train_test_split


# Fast processing sentiment140 for BERT training
# start reading in the files
t140 = pd.read_csv('training.1600000.processed.noemoticon.csv',
                   sep=',',
                   header=None,
                   encoding='latin')

label_text = t140[[0, 5]]

# Convert labels to range 0-1                                        
label_text[0] = label_text[0].apply(lambda x: 0 if x == 0 else 1)

# Assign proper column names to labels
label_text.columns = ['label', 'text']

# Assign proper column names to labels
label_text.head()

# preprocessing the tweet so that BERT will not overfitting on this
hashtags = re.compile(r"^#\S+|\s#\S+")
mentions = re.compile(r"^@\S+|\s@\S+")
urlsS = re.compile(r"https?://\S+")
urls = re.compile(r"http?://\S+")

def process_text(text):
  text = hashtags.sub(' hashtag', text)
  text = mentions.sub(' entity', text)
  return text.strip().lower()
  
def match_expr(pattern, string):
  return not pattern.search(string) == None

def get_data_wo_urlsS(dataset):
    link_with_urls = dataset.text.apply(lambda x: match_expr(urlsS, x))
    return dataset[[not e for e in link_with_urls]]

def get_data_wo_urls(dataset):
    link_with_urls = dataset.text.apply(lambda x: match_expr(urls, x))
    return dataset[[not e for e in link_with_urls]]

label_text.text = label_text.text.apply(process_text)

# split training and testing set
TRAIN_SIZE = 0.95
VAL_SIZE = 0.025
dataset_count = len(label_text)

df_train_val, df_test = train_test_split(label_text, test_size=1-TRAIN_SIZE-VAL_SIZE, random_state=42)
df_train, df_val = train_test_split(df_train_val, test_size=VAL_SIZE / (VAL_SIZE + TRAIN_SIZE), random_state=42)

print("TRAIN size:", len(df_train))
print("VAL size:", len(df_val))
print("TEST size:", len(df_test))

# final removing urls
df_train = get_data_wo_urls(df_train)
df_train = get_data_wo_urlsS(df_train)
df_train.head()

# output training developing testing dataset
df_train.sample(frac=1.0).reset_index(drop=True).to_csv('sentiment140/train.tsv', sep='\t', index=None, header=None)
df_val.to_csv('sentiment140/dev.tsv', sep='\t', index=None, header=None)
df_test.to_csv('sentiment140/test.tsv', sep='\t', index=None, header=None)


