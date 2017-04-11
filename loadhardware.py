import os
from subprocess import Popen, PIPE
from typeclassifier import TypeClassifier

class HardwareControl:
	
	def __init__(self):

		self.classifier = TypeClassifier("fastText/voiceai-hardware.bin", "fastText/fasttext")

		self.backlightDir = "/sys/class/backlight/acpi_video0/"
		self.maxBrightnessDir = self.backlightDir+'max_brightness'
		self.brightnessDir = self.backlightDir+'brightness'
		self.brightCmd = 'tee'
		f = open(self.maxBrightnessDir, 'r')
		self.max_brightness = int(f.readline())
		f.close()
		f = open(self.brightnessDir, 'r')
		self.brightness = int(f.readline())
		f.close()

		self.volumeCmd = "amixer set 'Master' "

	def textFilter(self, tagged):
		keep_words = ['xVB', 'xRP', 'xNN']
		change_tags = ['xCD']
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
		keep_words = ['xVB', 'xRP', 'xNN', 'xIN']
		change_tags = ['xCD']
		NUM = []
		# change tags -> keep tags -> return array of tuple

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

		text = [tup[0] for tup in filtered_tags]
		f_type, prob = self.classifier.classifyText(" ".join(text))

		msg = ""
		percent = 15
		if len(NUM) > 0:
			percent = int(NUM[0])
		if f_type == 1:
			return "".join([msg, self.increaseVolume(percent)])
		if f_type == 2:
			return "".join([msg, self.increaseVolume(percent, False)])
		if f_type == 3:
			return "".join([msg, self.increaseBrightness(percent)])
		if f_type == 4:
			return "".join([msg, self.increaseBrightness(percent, False)])
		if f_type == 5:
			return "".join([msg, self.setVolume(percent)])
		if f_type == 6:
			return "".join([msg, self.setBrightness(percent)])
		return "I'm sorry, I didn't get that"

	def setVolume(self, percent):
		os.system("".join([self.volumeCmd, str(percent), '%']))
		return "Volume set"

	def increaseVolume(self, percent, positive=True):
		sign = '+'
		if positive == False:
			sign = '-'
		os.system("".join([self.volumeCmd, str(percent), '%', sign]))
		return "Volume increased/decreased"

	def setBrightness(self, percent):
		if percent > 100:
			percent = 100

		if percent < 0:
			percent = 0

		self.brightness = int(percent*self.max_brightness/100)
		#sudoService = Popen(['sudo', '-S', 'su'], stdout=PIPE, stderr=PIPE)
		#o = sudoService.communicate(input='ironpatriot')
		os.system(" ".join(["echo", str(self.brightness), ">>", self.brightnessDir]))
		#brightnessService = Popen(["echo", " ".join(["2", ">>", self.brightnessDir])], stdout=PIPE, stderr=PIPE)
		#out = brightnessService.communicate(input='2')
		#sudoService = Popen(['exit'])
		return "Brightness set"

	def increaseBrightness(self, percent, positive=True):
		cPercent = self.brightness*100/self.max_brightness
		if positive:
			cPercent = cPercent + percent
		else:
			cPercent = cPercent - percent

		return self.setBrightness(cPercent)
