import os
from subprocess import Popen, PIPE

class HardwareControl:
	
	def __init__(self):
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
