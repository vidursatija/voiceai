from urllib.request import urlopen
import json
from pint import UnitRegistry

class ConversionControl:

	def __init__(self):
		self.ureg = UnitRegistry()

		self.exchUrl = "http://api.fixer.io/latest?symbols="

	def textFilter(self, tagged):
		keep_words = ['xWDT', 'xWRB', 'xVB', 'xIN']
		change_tags = ['xCD', 'xNN']
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
		keep_words = ['xIN']
		change_tags = ['xCD', 'xNNP']
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

	def convertUnit(self, unit1, quantity=1, type1='mks', type2='mks', unit2=None):
		
		return "Nothin"