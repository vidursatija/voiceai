# VOICEAI
Voiceai is a library for controlling a machine using text and voice based interface. It uses

1. The [Stanford NER tagger](http://nlp.stanford.edu/software/CRF-NER.shtml) for NER Tagging
2. The [Stanford Lex Parser](http://nlp.stanford.edu/software/lex-parser.shtml) for Lexical Tagging
3. The Facebook [fastText](https://github.com/facebookresearch/fastText) api for text classification

## Features 
### The following features are available with commands: 

1. Music control
  1. Play Song/Artist/Album
  2. Pause
  3. Stop
  4. Resume
Music library must be provided as json file.
Note : ML Algorithm for learning taste of music coming soon.
  
2. Hardware Control
  1. Adjust volume
  2. Adjust brightness (*needs root access*)
  
3. Conversion Control
  1. Convert units and dimensions (*coming soon*)
  2. Convert currencies (*internet required*) ([fixer.io](http://api.fixer.io/))
  
##### Coming Soon

4. Web search Control
  1. Search anything using the [DuckDuckGo](https://duckduckgo.com) api

5. Greeting Control
  1. Engage in a casual conversation with the bot

6. Alarm Control
  1. Set alarms and reminders

7. Wolfram Control
  1. Use Wolfram Alpha to get answers to mathematical answers

#### The following features are available using scripting:

1. Training
  1. Added new sentences for text classification (fastText)

### Installation
Place the voiceai directory in your project

```
git clone https://github.com/vidursatija/voiceai.git
```

### Usage

```python
import voiceai
VC = voiceai.VoiceAIControl()
print(VC.process_message("Play some Taylor Swift songs"))
print(VC.process_message("Increase brightness by 10%"))
print(VC.process_message("How many miles are there in a kilometer?"))
print(VC.process_message("Search the web for latest news"))
```
