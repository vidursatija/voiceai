from voiceai import VoiceAIControl
vc = VoiceAIControl()#["models/stanford-ner/voiceai-ner.ser.gz", "stanford-ner/stanford-ner.jar"], ["models/stanford-pos/voiceai-pos.tagger", "stanford-pos/stanford-postagger.jar"], ["models/fastText/voiceai.bin", "fastText/fasttext"])
print(vc.process_message("Please paint Taylor's car red"))

#from loadtrainer import TrainControl

#tc = TrainControl()
#tc.trainPOSTagger()
