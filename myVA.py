# -*- coding: utf-8 -*-
"""
Created on Mon May  15 13:46:31 2023

@author: Doug Nonast dnonast@gmail.com 
"""

import sys, os, platform
import openai
import speech_recognition as sr

#Platform specific settings and inits:
def platform_inits():
#ALSA lib will sometimes throw unecessary errors in Linux. Ignore them.
  if platform.system() == "Linux":
    from ctypes import CFUNCTYPE, c_char_p, c_int, cdll
    # Define error handler
    error_handler = CFUNCTYPE(None, c_char_p, c_int, c_char_p, c_int, c_char_p)
    # Don't do anything if there is an error message
    def py_error_handler(filename, line, function, err, fmt):
        pass
    # Pass to C
    c_error_handler = error_handler(py_error_handler)
    asound = cdll.LoadLibrary('libasound.so')
    asound.snd_lib_error_set_handler(c_error_handler)
  
  return

# Define the voice_to_text() function- no differenc between platforms
def voice_to_text():
  speech=sr.Recognizer()
  voice_input = "" 
  with sr.Microphone() as source:
    speech.adjust_for_ambient_noise(source)
    try:
        audio = speech.listen(source)
        voice_input = speech.recognize_google(audio)
    except sr.UnknownValueError:
        pass
    except sr.RequestError:
        pass 
    except sr.WaitTimeoutError:
        pass
  return voice_input
  
#Define text to voice functions
def text_to_voice(texts):
  #Windows pyttsx3 lets you define gender, speed, and volume of the speech
  if platform.system() == "Windows":
    #If we are in Windows, we need to use the pyttxs3 library
    import pyttsx3
    try:
      engine=pyttsx3.init()
    except ImportError:
      pass
    except RuntimeError:
      pass
    voices=engine.getProperty("voices")
    engine.setProperty("voice", voices[0].id)
    engine.setProperty("rate", 150)
    engine.setProperty("volume", 1.1)
    engine.say(texts)
    engine.runAndWait()
  #If it's not Windows, Mac and Linux use the same call:
  if platform.system() == "Darwin" or platform.system() == "Linux":
    texts = texts.replace('"','')
    texts = texts.replace("'","")
    #gtts can only change the speed. Add the --slow flag if you want slow speech
    os.system(f'gtts-cli --nocheck "{texts}" | mpg123 -q -')
  return

def call_chatgpt(user_request):
  #The chatgpt_key file has to be in the same folder as this script
  try:
     keyfile = os.path.realpath(os.path.dirname(__file__))+'/chatgpt_key.txt'
  except OSError:
     print("Error: Unable to open the key file chatgpt_key.txt, exiting.")
     sys.exit(1)
  #Handle the key being wrong:
  
  with open(keyfile, 'r') as file:
    openai.api_key = file.read().rstrip()

  try:
    completion = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=[
        {"role": "user", "content": user_request}
      ]
    )
    return_text=completion.choices[0].message.content
  except openai.error.RateLimitError:
    return_text = "The A.I. engine is overloaded right now. Please try again."
  except openai.error.AuthenticationError:
      print("Error: the Authentication key is incorrect. Exiting.")     
      sys.exit(1)
  return return_text

platform_inits()
show_text=False
while True:
  print("Listening...")
  inp=voice_to_text()
  if show_text: print(inp)
  if inp=="stop listening":
      text_to_voice("Goodbye!")
      break
  elif inp=="show text":
     print("Now showing text.")
     text_to_voice("Now showing text.")
     show_text=True
  elif inp=="stop text":
     print("Text will not show.")
     text_to_voice("Text will not show.")
     show_text=False     
  else:
      ai_resp = call_chatgpt(inp)
      if show_text: print(ai_resp)
      text_to_voice(ai_resp)
      continue
    