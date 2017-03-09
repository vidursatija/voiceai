# VOICEAI
Voiceai is a library for controlling a machine using text and voice based interface. It uses

1. The [Stanford NER tagger](http://nlp.stanford.edu/software/CRF-NER.shtml) for NER Tagging
2. The [Stanford POS tagger](http://nlp.stanford.edu/software/tagger.shtml) for POS Tagging
3. The Facebook [fastText](https://github.com/facebookresearch/fastText) api for text classification
4. The [CMU Sphinx](https://cmusphinx.sourceforge.net) api for voice recognition(**not added yet**)
5. The [pint](https://github.com/hgrecco/pint) library for cross units and dimensions conversion

## Features 
#### The following features are available with commands: 

1. Music control
  1. Play Song/Artist/Album
  2. Pause
  3. Stop
  4. Resume
  
2. Hardware Control
  1. Adjust volume
  2. Adjust brightness (*needs root access*)
  
3. Conversion Control
  1. Convert units and dimensions
  2. Convert currencies (*internet required*) ([fixer.io](http://api.fixer.io/))
  
4. Web search Control
  1. Search anything using the [DuckDuckGo](https://duckduckgo.com) api

5. Greeting Control
  1. Engage in a casual conversation with the bot

6. Alarm Control
  1. Set alarms and reminders

#### The following features are available using scripting:
1. Training
  1. Added new sentences and tokens for learning
  2. Train POS tagger, NER tagger, fastText with for better accuracy and language


### Installation
Place the voiceai directory in your project

```
git clone https://github.com/vidursatija/voiceai.git
```

### Usage

```python
import voiceai
print(voiceai.process_message("Play some Taylor Swift songs"))
print(voiceai.process_message("Increase brightness by 10%"))
print(voiceai.process_message("How many miles are there in a kilometer?"))
print(voiceai.process_message("Search the web for latest news"))
```
