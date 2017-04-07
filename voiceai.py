#NLP LIBs
import nltk
from nltk.tag.stanford import StanfordNERTagger
from nltk.tag.stanford import StanfordPOSTagger
from nltk.parse.stanford import StanfordDependencyParser

#SYSTEM LIBs
#import urllib.request
#import json
import os
import numpy as np

#MODULE CONTROLS
from loadmusic import MusicControl
from loadhardware import HardwareControl
from typeclassifier import TypeClassifier
from loadconversion import ConversionControl

class VoiceAIControl:
	def __init__(self):#, ner_dir, pos_dir, ft_dir):

		#MODELS_DIR, FASTTEXT_DIR, POS_DIR, NER_DIR, MUSIC_XML_DIR
		FASTTEXT_DIR = "fastText"
		MUSIC_DATABASE = "music_metadata.json"
		
		self.snt = StanfordNERTagger('stanford-ner/voiceai-ner.ser.gz', 'models/../stanford-ner/stanford-ner.jar')
		self.spt = StanfordPOSTagger('stanford-pos/voiceai_bi.tagger', 'models/../stanford-pos/stanford-postagger.jar') 
#		self.spt = StanfordPOSTagger('/run/media/vidur/Kachra/edu/stanford/nlp/models/pos-tagger/english-caseless-left3words-distsim.tagger', 'models/../stanford-pos/stanford-postagger.jar') 

		self.tyc = TypeClassifier("fastText/voiceai.bin", FASTTEXT_DIR+"/fasttext")#"fastText/voiceai.bin")

		self.controls = []
		self.controls.append(MusicControl(MUSIC_DATABASE))
		self.controls.append(HardwareControl())
		self.controls.append(ConversionControl())

		self.my_name = "Halzee"
		self.age = 16
		self.creator = "Vidur"

	def process_message(self, msg):
		msg_words = nltk.word_tokenize(msg)
		original_msg = msg

		#MESSAGE TYPE CLASSIFIERS:
		#1 - Music
		#2 - Brightness and Volume
		#3 - Units and Money
		#4 - Questions/Google/Wiki
		#5 - Alarm

		if msg_words[0] == self.my_name:
			if msg_words[1] == '.' or msg_words[1] == ',' :
				msg_words = msg_words[2:]
			else:
				msg_words = msg_words[1:]


		msg_words[0] = msg_words[0].lower()
		msg_words[0] = "".join([msg_words[0][0].upper(), msg_words[0][1:]])


		tags = self.spt.tag(msg_words)

		print(tags)

		tags, pure_entities = self.nerTaggerRun(tags)

		print(tags)
		print(pure_entities)

		# take tags -> run NER -> keep 000 tags as same, rest are converted to NNP

		all_filters = []
		for control in self.controls:
			all_filters.append(control.textFilter(tags))
		
		#all_types = []
		#all_probs = []
		final_type = -1
		max_count = -1
		type_counts = np.zeros(len(all_filters), dtype=int)

		for f in all_filters:
			text = [tup[0] for tup in f]
			t, p = self.tyc.classifyText(" ".join(text))
			#all_types.append(t)
			#all_probs.append(p)
			if t == -1:
				continue
			type_counts[t-1] = type_counts[t-1] + 1

		for i, ct in enumerate(type_counts):
			if ct > max_count:
				max_count = ct
				final_type = i
		
		print(self.controls[final_type].functionFilter(tags, pure_entities))

		"""
		
		if textType == 3:
			quantity = 1
			if len(NUM) > 0:
				quantity = float(NUM[0][1])

			print(Money)

			if len(Money) > 1:
				return "".join([msg, self.cc.convertMoney(Money[0], quantity, Money[1])])
			else:
				if len(Money) > 0:
					return "".join([msg, self.cc.convertMoney(Money[0], quantity)])
				else:
					return msg

		if textType == 4:
			return "".join([msg, "Search request"])
		"""

	def nerTaggerRun(self, tags):
		#filter_tags = ['NN', 'NNP', 'CD']
		entities = []
		ct = -1
		prev_entity = False
		for i, tup in enumerate(tags):
			if tup[1] == 'xNN' or tup[1] == 'xNNP':
				if prev_entity == True:
					entities[ct].append((i, tup[0]))
				else:
					ct = ct + 1
					entities.append([])
					entities[ct].append((i, tup[0]))
					prev_entity = True
			else:
				prev_entity = False

		#print(entities)

		pure_entities = []
		ct = -1
		prev_entity = False
		for i, entity in enumerate(entities):
			text = [tup[1] for tup in entity]
			ner_tags = self.snt.tag(text)
			#print(ner_tags)
			prev_entity = False
			for j, ner_tag in enumerate(ner_tags):
				if ner_tag[1] == 'OOO':
					prev_entity = False
				else:
					#print(i, j)
					tags[entities[i][j][0]] = (tags[entities[i][j][0]][0], 'xNNP')
					if prev_entity == True:
						pure_entities[ct].append(ner_tag)
					else:
						ct = ct + 1
						pure_entities.append([])
						pure_entities[ct].append(ner_tag)
						prev_entity = True

			#print(pure_entities)
		return tags, pure_entities