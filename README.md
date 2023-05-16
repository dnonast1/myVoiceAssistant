# myVoiceAssistant
Python script to listen to speech from the user, send that to chatGPT, then read back the response. Similar to Amazon Echo or Apple Siri.

By Doug Nonast 
dnonast@gmail.com

Uses code based on: 

[Make Python Talk](https://github.com/markhliu/mpt)
  
[ThePyCoach](https://medium.com/geekculture/a-simple-guide-to-chatgpt-api-with-python-c147985ae28)

## Requirements:
-Installation of the following modules:

	openai
	speechrecognition
 	pyttsx3 (if on Windows)
		
-A file named chatgpt_key.txt must be in the same directory as the script and must consist of a single line containing only the chatGPT token. This is individual to the user and is available from the [chatGPT Website](https://beta.openai.com/account/api-keys)

## Commands
The following commands can be spoken and will not be passed to chatGPT:

- **"show text"** This will show the text being spoken or heard. Default is not to show text.
- **"stop text"** This will prevent text from being shown when spoken or heard.
- **"stop listening"** This will exit the program

## ToDo:
History is currently forgotten after each chatGPT call. Next rev will keep history allowing the user to follow up a question of "Who was George Washington?" with "Who was he married to?"


