#NLP LIBs
import nltk
from nltk.tag.stanford import StanfordNERTagger
from nltk.tag.stanford import StanfordPOSTagger
from nltk.parse.stanford import StanfordDependencyParser

#SYSTEM LIBs
#import urllib.request
#import json
import os
from pprint import pprint

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
		
		self.snt = StanfordNERTagger('models/stanford-ner/voiceai-ner.ser.gz', 'models/../stanford-ner/stanford-ner.jar')
		self.spt = StanfordPOSTagger('stanford-pos/models/english-left3words-distsim.tagger', 'models/../stanford-pos/stanford-postagger.jar') 
#		self.spt = StanfordPOSTagger('/run/media/vidur/Kachra/edu/stanford/nlp/models/pos-tagger/english-caseless-left3words-distsim.tagger', 'models/../stanford-pos/stanford-postagger.jar') 

		self.tyc = TypeClassifier("fastText/voiceai.bin", FASTTEXT_DIR+"/fasttext")#"fastText/voiceai.bin")

		self.mp  = MusicControl(MUSIC_DATABASE)		
		self.hc  = HardwareControl()
		self.cc  = ConversionControl()

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

		#CATCH POS
		
		"""if tup[1] == 'NUM' or tup[1] == 'ENT':
			function_text.append(tup[1])
		else:
			function_text.append(tup[0]) 

		tag_text = tag_text + tup[1] + " "

		saveF = open("allTexts.tsv", 'a')
		saveF.write(msg)
		saveF.write('\n')
		saveF.close()

		print(tag_text)
		print(classify_text)
		print(function_text)

		textType, prob = self.tyc.classifyText(classify_text)
		if textType > -1:
			msg="__label__"+str(textType)
			print("Prob : "+prob)
		else:
			return "I'm sorry I didn't get that, Vidur"

		TypeClassifierFile = open("fastText/voiceai-train.tsv", 'a')
		TypeClassifierFile.write("__label__"+str(textType)+" , "+classify_text.lower()+'\n')
		TypeClassifierFile.close()
		
		#CATCH ENTITIES
		entities = []
		ct = -1
		prevEntity = False
		for i, tup in enumerate(ENT):
			if tup[1] == 'ENT':
				if prevEntity == True:
					entities[ct].append(tup[0])
				else:
					ct = ct + 1
					entities.append([])
					entities[ct].append(tup[0])
					prevEntity = True
			else:
				prevEntity = False

		#CATCH ENTITY TYPES
		People = []
		Organisations = []
		Artworks = []
		Locations = []
		Time = []
		Date = []
		Money = []
		
		msg = "".join([msg, "\nEntities : "])
		for entity in entities:
			pos_tagged = self.snt.tag(entity)
			msg2 = " ".join(["-".join([x[0], x[1]]) for x in pos_tagged])
			msg = "\n".join([msg, msg2])
			if pos_tagged[0][1] == 'PER':
				People.append(" ".join([x[0] for x in pos_tagged]))
			if pos_tagged[0][1] == 'ART':
				Artworks.append(" ".join([x[0] for x in pos_tagged]))
			if pos_tagged[0][1] == 'ORG':
				Organisations.append(" ".join([x[0] for x in pos_tagged]))
			if pos_tagged[0][1] == 'LOC':
				Locations.append(" ".join([x[0] for x in pos_tagged]))
			if pos_tagged[0][1] == 'TIM':
				Time.append(" ".join([x[0] for x in pos_tagged]))
			if pos_tagged[0][1] == 'DAT':
				Date.append(" ".join([x[0] for x in pos_tagged]))
			if pos_tagged[0][1] == 'MON':
				Money.append(" ".join([x[0] for x in pos_tagged]))

		#SELECT TYPE CONTROL
		#print(new_text)
		if textType == 1:
			#TYPE MUSIC			
			musicClassifier = TypeClassifier("fastText/voiceai-music.bin", "fastText"+"/fasttext")
			musicType, prob = musicClassifier.classifyText(" ".join(function_text))
			if musicType > -1:
				print("Prob : "+prob)
			else:
				return "I'm sorry I didn't get that, Vidur"

			song_name = None
			artist_name = None
			album_name = None

			if len(People) > 0:
				artist_name = People[0]

			if len(Artworks) > 0:
				song_name = Artworks[0]

			if len(Artworks) > 1:
				album_name = Artworks[1] 
			
			print(musicType)
			TypeClassifierFile = open("fastText/voiceai-music.tsv", 'a')
			TypeClassifierFile.write("__label__"+str(musicType)+" , "+" ".join(function_text).lower()+'\n')
			TypeClassifierFile.close()
			if musicType == 1:
				return "\n".join([msg, "Playing song :", self.mp.Play(song_name, artist_name, album_name)])#self.mp.Play(song_name, artist_name, album_name)])
			if musicType == 2:
				return "\n".join([msg, self.mp.Stop()])
			if musicType == 3:
				return "\n".join([msg, self.mp.Pause()])
			if musicType == 4:
				return "\n".join([msg, self.mp.Next()])
			if musicType == 5:
				return "\n".join([msg, self.mp.Prev()])
			textType = 4
		
		if textType == 2:
			hardwClassifier = TypeClassifier("fastText/voiceai-hardware.bin", "fastText"+"/fasttext")
			hardwType, prob = hardwClassifier.classifyText(" ".join(function_text))
			if hardwType > -1:
				print("Prob : "+prob)
			else:
				return "I'm sorry I didn't get that, Vidur"

			print(hardwType)
			TypeClassifierFile = open("fastText/voiceai-hardware.tsv", 'a')
			TypeClassifierFile.write("__label__"+str(hardwType)+" , "+" ".join(function_text).lower()+'\n')
			TypeClassifierFile.close()
			textType = 4
			percent = 15
			if len(NUM) > 0:
				percent = int(NUM[0][1])
			if hardwType == 1:
				return "".join([msg, self.hc.increaseVolume(percent)])
			if hardwType == 2:
				return "".join([msg, self.hc.increaseVolume(percent, False)])
			if hardwType == 3:
				return "".join([msg, self.hc.increaseBrightness(percent)])
			if hardwType == 4:
				return "".join([msg, self.hc.increaseBrightness(percent, False)])
			if hardwType == 5:
				return "".join([msg, self.hc.setVolume(percent)])
			if hardwType == 6:
				return "".join([msg, self.hc.setBrightness(percent)])


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
