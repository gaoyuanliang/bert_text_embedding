###########jessica_text_embedding.py###########
'''
https://storage.googleapis.com/bert_models/2019_05_30/wwm_uncased_L-24_H-1024_A-16.zip

https://storage.googleapis.com/bert_models/2019_05_30/wwm_cased_L-24_H-1024_A-16.zip

https://github.com/CyberZHG/keras-bert/blob/e9ccba8ed56b52102bfd08fd231bf9b79d7e0e3e/keras_bert/util.py#L34

tensorflow==2.2.0
keras==2.4.3
keras_bert==0.86.0
'''

import numpy as np
from keras_bert import *
from keras.models import Model
from keras_bert.layers import Extract, MaskedGlobalMaxPool1D
from keras.layers import GlobalAvgPool1D, Concatenate
from keras.preprocessing.sequence import pad_sequences

model_path = 'wwm_uncased_L-24_H-1024_A-16'

paths = get_checkpoint_paths(model_path)
token_dict = load_vocabulary(paths.vocab)
tokenizer = Tokenizer(token_dict)

model = load_trained_model_from_checkpoint(
	paths.config, paths.checkpoint, 
	output_layer_num = 1)
#model.summary(line_length=120)

outputs = [
	Extract(index=0, name='Pool-NSP')(model.outputs[0]),
	MaskedGlobalMaxPool1D(name='Pool-Max')(model.outputs[0]),
	#GlobalAvgPool1D(name='Pool-Ave')(model.outputs[0]),
	]
outputs = Concatenate(name='Concatenate')(outputs)

model_sentence_emb = Model(
	inputs=model.inputs, 
	outputs=outputs)

def text_embedding(input):
	try:
		word_idx = np.array([[token_dict[token] for token in tokenizer.tokenize(input)]])
		word_idx = pad_sequences(word_idx, maxlen = 512)
		segments = np.zeros(word_idx.shape)
		text_emb = model_sentence_emb.predict([word_idx, segments])
		return text_emb[0].tolist()
	except:
		return None
###########jessica_text_embedding.py###########
