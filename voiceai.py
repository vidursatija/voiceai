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
		self.sdp = StanfordDependencyParser(path_to_jar="models/../stanford-parser/stanford-parser.jar", path_to_models_jar="/run/media/vidur/Kachra/stanford-english-corenlp-2016-10-31-models.jar")

		self.tyc = TypeClassifier("fastText/voiceai.bin", FASTTEXT_DIR+"/fasttext")#"fastText/voiceai.bin")

		self.mp  = MusicControl(MUSIC_DATABASE)		
		self.hc  = HardwareControl()
		self.cc  = ConversionControl()

		self.myName = "Halzee"
		self.age = 16
		self.creator = "Vidur"

	def process_message(self, msg):
		msg_words = nltk.word_tokenize(msg)
		#msg_words[0] = msg_words[0].lower()
		original_msg = msg
		#MESSAGE TYPE CLASSIFIERS:
		#1 - Music
		#2 - Brightness and Volume
		#3 - Units and Money


		if msg_words[0] == self.myName:
			if msg_words[1] == '.' or msg_words[1] == ',' :
				msg_words = msg_words[2:]
			else:
				msg_words = msg_words[1:]


		msg_words[0] = msg_words[0].lower()
		msg_words[0] = "".join([msg_words[0][0].upper(), msg_words[0][1:]]) 

		#CATCH POS
		#tags = [('turn', 'VB'), ('some', 'DT'), ('Taylor', 'NNP'), ('Swift', 'NNP'), ('songs', 'NNS'), ('on', 'RP')]#self.spt.tag(msg_words)
		tags = self.spt.tag(msg_words)



		entities = []
		ct = -1
		prevEntity = False
		for i, tup in enumerate(tags):
			if tup[1] == 'NNP' or tup[1] == 'NNPS':
				if prevEntity == True:
					entities[ct].append(tup[0])
					#tup[0] = 'ENTITY'
					tags.pop(i)
				else:
					ct = ct + 1
					entities.append([])
					entities[ct].append(tup[0])
					tags[i] = ("ENTITY_"+str(ct), tup[1])
					prevEntity = True
			else:
				prevEntity = False

		#tags[0] = ('1', tags[0][1])

		parsed = self.sdp.tagged_parse(tags)
		print(tags)
		pars = [par for par in parsed]
		relations = [list(par.triples()) for par in pars]
		relations = relations[0]
		sent_tree = [par.tree() for par in pars]
		print(relations)

		#find relations
		Advmod   = []
		Amod     = []
		Case     = []
		Compound = []
		CmpdPrt  = []
		Det      = []
		Dobj     = []
		Nmod     = []
		Nsubj    = []
		Xcomp    = []

		for tup in relations:
			if tup[1] == 'advmod':
				Advmod.append((tup[0], tup[2]))
			else:
				if tup[1] == 'amod':
					Amod.append((tup[0], tup[2]))
				else:
					if tup[1] == 'case':
						Case.append((tup[0], tup[2]))
					else:
						if tup[1] == 'compound':
							Case.append((tup[0], tup[2]))
						else:
							if tup[1] == 'compound:prt':
								CmpdPrt.append((tup[0], tup[2]))
							else:
								if tup[1] == 'det':
									Det.append((tup[0], tup[2]))
								else:
									if tup[1] == 'nmod':
										Nmod.append((tup[0], tup[2]))
									else:
										if tup[1] == 'nsubj':
											Nsubj.append((tup[0], tup[2]))
										else:
											if tup[1] == 'xcomp':
												Xcomp.append((tup[0], tup[2]))
											else:
												if tup[1] == 'dobj':
													Dobj.append((tup[0], tup[2]))




		#print(sent_tree[0].pretty_print())
		#print(sent_tree)
		#print([list(par.triples()) for par in parsed])# for parse in parsed])# self.sdp.raw_parse(msg)])
		#print([par.tree().pretty_print() for par in parsed])# for parse in parsed])# self.sdp.raw_parse(msg)])
		"""
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
