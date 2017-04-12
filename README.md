# VOICEAI
Voiceai is a library for controlling a machine using text and voice based interface. It uses

1. The [Stanford NER tagger](http://nlp.stanford.edu/software/CRF-NER.shtml) for NER Tagging
2. The [Stanford POS tagger](http://nlp.stanford.edu/software/tagger.shtml) for POS Tagging
3. The Facebook [fastText](https://github.com/facebookresearch/fastText) for text classification
4. The [pint](https://pint.readthedocs.io/en/0.7.2/) library for converting units
5. The [fixer.io](http://api.fixer.io/) api for converting currencies
6. The [duckduckgo](https://github.com/crazedpsyc/python-duckduckgo) wrapper for searching

## Features 

### The following features are available with commands: 

1. Music control
  * Play Song/Artist/Album
  * Pause
  * Stop
  * Resume

Music library must be provided as json file.

Note : ML Algorithm for learning taste of music coming soon.
  
2. Hardware Control
  * Adjust volume
  * Adjust brightness (*needs root access*)
  
3. Conversion Control
  * Convert units and dimensions
  * Convert currencies (*internet required*)

4. Web search Control
  * Search anything using the [DuckDuckGo](https://duckduckgo.com) api

##### Coming Soon

5. Greeting Control
  * Engage in a casual conversation with the bot

6. Alarm Control
  * Set alarms and reminders

7. Wolfram Control
  * Use Wolfram Alpha to get answers to mathematical answers

#### The following features are available using scripting:

1. Training
  * Add new sentences for text classification (fastText)
  * Add new NER tags for better support (Stanford-NER)
  * Add new POS tags for better support (Stanford-POSTagger)

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
```
