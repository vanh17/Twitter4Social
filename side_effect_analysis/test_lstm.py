from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from keras.models import Model
from keras.layers import GRU, Activation, Dense, Dropout, Input, Embedding
from keras.optimizers import RMSprop
from keras.preprocessing.text import Tokenizer
from keras.preprocessing import sequence
from keras.utils import to_categorical
from keras.callbacks import EarlyStopping
from keras.models import load_model
import re
import pandas as pd

# before we do this, we might need to add one head row in the
# training.1600000 file, "v1", "v3", "v4", "v5", "v6", "v2"
df = pd.read_csv('training.1600000.processed.noemoticon.csv',delimiter=',',encoding='latin-1')
# we need this or else it wont be in approriate shapte for le.fit_transform
df.head()

df.drop(df.columns[1], axis=1, inplace=True)
df.drop(df.columns[1], axis=1, inplace=True)
df.drop(df.columns[1], axis=1, inplace=True)
df.drop(df.columns[1], axis=1, inplace=True)
df.info()

X = df.v2
Y = df.v1
le = LabelEncoder()
Y = le.fit_transform(Y)
Y = Y.reshape(-1,1)

X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.05)

# initial the model
model = load_model('lstm.h5')
max_words = 10000
max_len = 128
tok = Tokenizer(num_words=max_words)
tok.fit_on_texts(X_train)


# preprocessing the tweet so that BERT will not overfitting on this
hashtags = re.compile(r"^#\S+|\s#\S+")
mentions = re.compile(r"^@\S+|\s@\S+")
urlsS = re.compile(r"https?://\S+")
urls = re.compile(r"http?://\S+")

def process_text(text):
  text = hashtags.sub(' hashtag', text)
  text = mentions.sub(' entity', text)
  text = urls.sub(' urls', text)
  text = urlsS.sub(' urls', text)
  return text.strip().lower()
  
tweets1 = open("twtstatetime1.txt", "r")
tweets2 = open("twtstatetime2.txt", "r")

tweets1 = tweets1.readlines()
tweets2 = tweets2.readlines()

tweets1_categorized = open("twtstatetime_categorizedLSTM.txt", "w")

print("Start categorizing first half")
for twt in tweets1:
	twt = twt.strip("\n")
	twt_splted = twt.split("\t")
	text = process_text(twt_splted[2])
	text = tok.texts_to_sequences(text)
	text = sequence.pad_sequences(text, maxlen=max_len)
	predicted_stat = model.predict([text])
	label = "0"
	if predicted_stat[0] < predicted_stat[1]:
		label = "1"
	tweets1_categorized.write(twt + "\t" + label + "\n")

print("Start categorizing second half")
for twt in tweets2:
	twt = twt.strip("\n")
	twt_splted = twt.split("\t")
	text = process_text(twt_splted[2])
	text = tok.texts_to_sequences(text)
	text = sequence.pad_sequences(text, maxlen=max_len)
	predicted_stat = model.predict([text])
	label = "0"
	if predicted_stat[0] < predicted_stat[1]:
		label = "1"
	tweets1_categorized.write(twt + "\t" + label + "\n")