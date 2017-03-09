from urllib.request import urlopen
import json
from pint import UnitRegistry

class ConversionControl:

	def __init__(self):
		self.ureg = UnitRegistry()

		self.exchUrl = "http://api.fixer.io/latest?symbols="

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