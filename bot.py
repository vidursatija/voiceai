#BOT and NETWORK LIBs
from flask import Flask, request
from pymessenger.bot import Bot
from voiceai import VoiceAIControl
import urllib.request
from pydub import AudioSegment
from os import environ, path
import os

from pocketsphinx.pocketsphinx import *
from sphinxbase.sphinxbase import *

MODELDIR = "pocketsphinx-5prealpha/model"
DATADIR = ""

config = Decoder.default_config()
config.set_string('-hmm', path.join(MODELDIR, 'en-us/en-us'))
config.set_string('-lm', path.join(MODELDIR, 'en-us/en-us.lm.bin'))
config.set_string('-dict', path.join(MODELDIR, 'en-us/cmudict-en-us.dict'))
decoder = Decoder(config)

# Decode streaming data.
decoder = Decoder(config)

AI = VoiceAIControl(["models/stanford-ner/voiceai-ner.ser.gz", "stanford-ner/stanford-ner.jar"], ["models/stanford-pos/voiceai-pos.tagger", "stanford-pos/stanford-postagger.jar"], ["models/fastText/voiceai.bin", "fastText/fasttext"])#VoiceAIControl()

app = Flask(__name__)

ACCESS_TOKEN = "EAADY5DbIKHMBANJuls1tuvUqk9ZA8zdxUsDk2sF3fNR3XfQpvmrwsrIctyNsVkZCakWX4zkELXUgkWYJL7Jvls4KuLZCrr3QtZCmVRHCTv1A8G4bozrsN80hdKuicnk54Hs0N9ieJDQZB4cZAlIYUrKUslpWVFWVO6rPXxfQ8AtgZDZD"
VERIFY_TOKEN = "ironpatriot"
bot = Bot(ACCESS_TOKEN)
recipient_id = None

@app.route("/", methods=['GET', 'POST'])
def hello():
    if request.method == 'GET':
        if request.args.get("hub.verify_token") == VERIFY_TOKEN:
            return request.args.get("hub.challenge")
        else:
            return 'Invalid verification token'

    if request.method == 'POST':
        output = request.get_json()
        for event in output['entry']:
            messaging = event['messaging']
            for x in messaging:
                if x.get('message'):
                    recipient_id = x['sender']['id']
                    if x['message'].get('text'):
                        message = x['message']['text']
                        msg =  AI.process_message(message)
                        
                        bot.send_text_message(recipient_id, msg)
                    if x['message'].get('attachments'):
                        for att in x['message'].get('attachments'):
                            print(att['payload']['url'])
                            voice_url = urllib.request.urlopen(att['payload']['url'])
                            with open('voicemsg.aac', 'w+b') as f:
                                f.write(voice_url.read())
                            f.close()
                            aac_file = AudioSegment.from_file('voicemsg.aac', format='aac')
                            wav_handler = aac_file.export('rawmsg.wav', format='wav')
                            os.system("sox rawmsg.wav -r 16000 temp.wav")
                            wav_handler = AudioSegment.from_file('temp.wav', format='wav')
                            raw_handler = wav_handler.export('rawmsg.raw', format='raw')
                            decoder.start_utt()
                            stream = open('rawmsg.raw', 'rb')
                            #stream.seek(44)
                            while True:
                                buf = stream.read(1024)
                                if buf:
                                    decoder.process_raw(buf, False, False)
                                else:
                                    break
                            decoder.end_utt()
                            sentence = " ".join([seg.word for seg in decoder.seg()])
                            bot.send_text_message(recipient_id, sentence)
                            #bot.send_attachment_url(recipient_id, att['type'], att['payload']['url'])
                else:
                    pass
        return "Success"


if __name__ == "__main__":
    app.run(port=5000, debug=True)

