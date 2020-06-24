from BertLibrary import BertFTModel
import re

# initial the model
ft_model = BertFTModel( model_dir='sentiment140/uncased_L-12_H-768_A-12',
                         ckpt_name="bert_model.ckpt",
                         labels=['0','1'],
                         lr=5e-06,
                         num_train_steps=60000,
                         num_warmup_steps=1000,
                         ckpt_output_dir='sentiment140/output',
                         save_check_steps=1000,
                         do_lower_case=False,
                         max_seq_len=64,
                         batch_size=32,
                         )

ft_predictor = ft_model.get_predictor()




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

tweets1_categorized = open("twtstatetime1_categorized.txt", "w")
tweets2_categorized = open("twtstatetime2_categorized.txt", "w")

print("Start categorizing first half")
for twt in tweets1:
	twt = twt.strip("\n")
	twt_splted = twt.split("\t")
	text = process_text(twt_splted[2])
	predicted_stat = ft_predictor([text])[0]
	label = "0"
	if predicted_stat[0] < predicted_stat[1]:
		label = "1"
	tweets1_categorized.write(twt + "\t" + label + "\n")

print("Start categorizing second half")
for twt in tweets2:
	twt = twt.strip("\n")
	twt_splted = twt.split("\t")
	text = process_text(twt_splted[2])
	predicted_stat = ft_predictor([text])[0]
	label = "0"
	if predicted_stat[0] < predicted_stat[1]:
		label = "1"
	tweets2_categorized.write(twt + "\t" + label + "\n")