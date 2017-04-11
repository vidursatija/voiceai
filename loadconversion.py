from urllib.request import urlopen
import json
from pint import UnitRegistry
from random import Random
from typeclassifier import TypeClassifier

class ConversionControl:

	def __init__(self):

		self.classifier = TypeClassifier("fastText/voiceai-conversion.bin", "fastText/fasttext")

		self.ureg = UnitRegistry()

		self.exchUrl = "http://api.fixer.io/latest?symbols="

		self.randomizer = Random()
		self.conversion_fail = ["Are you okay?", "Wtf bro?", "Any more wrong conversions?", "Are you Ayesha?", "That was Burhan level", "Shravika level exceeded"]

	def textFilter(self, tagged):
		keep_words = ['xWDT', 'xWRB', 'xVB', 'xIN', 'xTO']
		change_tags = ['xCD', 'xNN', 'xNNP']
		# change tags -> keep tags -> return array of tuple

		filtered_tags = []
		for tup in tagged:
			for k_w in keep_words:
				if tup[1] == k_w:
					filtered_tags.append(tup)
					break

			for c_t in change_tags:
				if tup[1] == c_t:
					filtered_tags.append((tup[1], tup[1]))
					break

		return filtered_tags

	def functionFilter(self, tagged, pure_entities):
		keep_words = ['xIN', 'xTO']
		change_tags = ['xCD', 'xNNP']
		# change tags -> keep tags -> return array of tuple
		NUM  = []

		filtered_tags = []
		for tup in tagged:
			for k_w in keep_words:
				if tup[1] == k_w:
					filtered_tags.append(tup)
					break

			if tup[1] == 'xCD':
				NUM.append(int(tup[0]))

			for c_t in change_tags:
				if tup[1] == c_t:
					filtered_tags.append((tup[1], tup[1]))
					break

		if len(pure_entities) == 0 or len(pure_entities) > 2:
			return self.conversion_fail[self.randomizer.randint(0, len(self.conversion_fail)-1)]

		if len(pure_entities) == 2 and pure_entities[0][0][1] != pure_entities[1][0][1]:
			return self.conversion_fail[self.randomizer.randint(0, len(self.conversion_fail)-1)]

		text = [tup[0] for tup in filtered_tags]
		f_type, prob = self.classifier.classifyText(" ".join(text))
		print(text)
		# Type 1 - xCD xNNP xNNP
		# Type 2 - xNNP xCD xNNP

		msg = ""
		print(prob)

		if f_type == 1:
			amount = 1
			if len(NUM) > 0:
				amount = NUM[0]

			conversion_ent = pure_entities[0][0][1]
			if conversion_ent == 'MON':
				if len(pure_entities) == 2:
					return self.convertMoney(pure_entities[0][0][0], amount, pure_entities[1][0][0])
				else:
					return self.convertMoney(pure_entities[0][0][0], amount)
			else:
				if conversion_ent == 'QTY':
					if len(pure_entities) == 2:
						unit1 = [t[0] for t in pure_entities[0]]
						unit2 = [t[0] for t in pure_entities[1]]
						return self.convertUnit(unit1, amount, unit2)
					else:
						unit1 = [t[0] for t in pure_entities[0]]
						return self.convertUnit(unit1, amount)
				else:
					return self.conversion_fail[self.randomizer.randint(0, len(self.conversion_fail)-1)]				
		
		if f_type == 2:
			amount = 1
			if len(NUM) > 0:
				amount = NUM[0]

			conversion_ent = pure_entities[0][0][1]
			if conversion_ent == 'MON':
				return self.convertMoney(pure_entities[1][0][0], amount, pure_entities[0][0][0])
			else:
				if conversion_ent == 'QTY':
					unit1 = [t[0] for t in pure_entities[0]]
					unit2 = [t[0] for t in pure_entities[1]]
					return self.convertUnit(unit2, amount, unit1)
				else:
					return self.conversion_fail[self.randomizer.randint(0, len(self.conversion_fail)-1)]
		
		return self.conversion_fail[self.randomizer.randint(0, len(self.conversion_fail)-1)]

	def convertMoney(self, from_m, quantity = 1, to_m = 'INR'):

		jsonData = urlopen("".join([self.exchUrl, to_m, ",", from_m])).read()
		data = json.loads(jsonData)
		try:
			if from_m == 'EUR':
				r_from = 1#data["base"]
				r_to   = data["rates"][to_m]
			else:
				if to_m == 'EUR':
					r_from = data["rates"][from_m]
					r_to   = 1#data["base"]
				else:
					r_from = data["rates"][from_m]
					r_to   = data["rates"][to_m]
		except Exception as e:
			return "Currency error"


		conversion = quantity*r_to/r_from

		return " ".join([str(quantity), from_m, "is equal to", str(conversion), to_m])

	def convertUnit(self, unit1, quantity=1, unit2=None):
		if unit2 == None:
			try:
				q = (quantity * self.ureg('_'.join(unit1))).to_base_units()
			except Exception as e:
				print(e)
				return self.conversion_fail[self.randomizer.randint(0, len(self.conversion_fail)-1)]

			return " ".join([str(quantity), " ".join(unit1), "is equal to", str(q.magnitude), str(q.units)])
		else:
			try:
				q = (quantity * self.ureg('_'.join(unit1))).to(self.ureg('_'.join(unit2)))
			except Exception as e:
				print(e)
				return self.conversion_fail[self.randomizer.randint(0, len(self.conversion_fail)-1)]

			return " ".join([str(quantity), " ".join(unit1), "is equal to", str(q.magnitude), " ".join(unit2)])