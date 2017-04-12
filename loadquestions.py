from urllib.request import urlopen
import json
from random import Random
from typeclassifier import TypeClassifier
import duckduckgo

class QuestionControl:

	def __init__(self):

		self.classifier = TypeClassifier("fastText/voiceai-questions.bin", "fastText/fasttext")

		self.randomizer = Random()
		self.search_fail = ["Are you okay?", "Wtf bro?", "Anymore wrong searches?", "Are you Ayesha?", "That was Burhan level", "Shravika level exceeded"]

	def search(self, text):
		try:
			return duckduckgo.get_zci(text)
		except Exception as e:
			print(e)
			return self.search_fail[self.randomizer.randint(0, len(self.search_fail)-1)]