import os
from subprocess import Popen, PIPE

class TrainControl():

	def __init__(self):
		self.posAddDir = 'models/stanford-pos/newText.tsv'
		self.posOrigDir = 'models/stanford-pos/brownCorp.tsv'
		self.posTrainDir = 'models/stanford-pos/trainpos.tsv'
		self.posModelDir = 'models/stanford-pos/voiceai-pos.tagger'
		self.posPropsDir = 'models/stanford-pos/voiceai-pos.tagger.props'
		self.posTaggerDir = 'stanford-pos/stanford-postagger.jar'

		self.nerAddDir = 'models/stanford-ner/extras.tsv'
		self.nerMusicDir = 'models/stanford-ner/musicxml.tsv'
		self.nerModelDir = 'models/stanford-ner/voiceai-ner.ser.gz'
		self.nerPropsDir = 'models/stanford-ner/voiceai-ner.prop'
		self.nerTaggerDir = 'stanford-ner/stanford-ner.jar'

		self.ftAddDir = 'models/fastText/voiceai-train.tsv'
		self.ftModelDir = 'models/fastText/voiceai'
		self.ftSupervisedDir = 'fastText/fasttext'
	
	def addPOSTagger(self, msg):
		#os.chdir('stanford-pos')
		addfile = open(self.posAddDir, 'a')
		addfile.write(msg)
		addfile.write('\n')
		addfile.close()
		#os.chdir('..')

	def trainPOSTagger(self):
		#os.chdir('stanford-pos')
		trainfile = open(self.posTrainDir, 'w')
		addfile = open(self.posAddDir, 'r')
		brownfile = open(self.posOrigDir, 'r')

		for line in brownfile:
			trainfile.write(line)

		for line in addfile:
			trainfile.write(line)

		trainfile.close()
		addfile.close()
		brownfile.close()
		#os.chdir('..')
		#trainProcess = Popen(["java", "-mx1g", "-cp", self.posTaggerDir, "edu.stanford.nlp.tagger.maxent.MaxentTagger", "-props", self.posPropsDir])

	def addNERTagger(self, msg):
		os.chdir('stanford-ner')
		words = msg.split()
		tag = words[-1].upper()
		tokens = words[:-1]

		addfile = open(self.nerAddDir, 'a')
		for token in tokens:
			addfile.write(token)
			addfile.write('\t')
			addfile.write(tag)
			addfile.write('\n')

		addfile.write('\n')
		addfile.close()
		os.chdir('..')

	def trainNERTagger(self):
		os.chdir('stanford-ner')
		trainProcess = Popen(["java", "-mx1g", "-cp", self.nerTaggerDir, "edu.stanford.nlp.ie.crf.CRFClassifier", "-prop", self.nerPropsDir])
		os.chdir('..')
	def addFt(self, msg):
		addfile = open(self.ftAddDir, 'a')
		words = msg.split()
		msg = msg.lower()
		label = words[-1]
		tokens = words[:-1]
		addfile.write("".join(['__label__', label, ' , ']))
		addfile.write(" ".join(tokens))
		addfile.close()

	def trainFt(self):
		trainProcess = Popen([self.ftSupervisedDir, "supervised", "-input", self.ftAddDir, "-output", self.ftModelDir])
