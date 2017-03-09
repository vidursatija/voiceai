import os
from subprocess import Popen, PIPE

class TypeClassifier():
	
	def __init__(self, modelDir, execDir):
		self.mdir = modelDir
		self.edir = execDir

	def classifyText(self, text):
		text = text.lower()
		f = open("tmp.dat", 'w')
		f.write(text)
		f.close()

		process = Popen([self.edir, "predict", self.mdir, "tmp.dat"], stdout=PIPE, stderr=PIPE)
		out, err = process.communicate()
	
		line = str(out, 'utf-8')
		if len(line) > 8:
			num = int(line[9:])
		else:
			num = -1
		#print(out)		
		return num

