from google import generativeai as genai
import os
from dotenv import load_dotenv


load_dotenv('env/.env')
AI_preText = None

def set_AI():
  '''
  this is setting up the google's 2.0-flash gemini model // you can try with different models as well
  '''
  
  # some pre-instructions to the AI model
  global AI_preText
  
  with open('model/geminiMsg.txt') as file:
    AI_preText = file.read()
  
  # setting up configuration
  genai.configure(api_key=os.getenv('gemini_apiKey'))
  
  # getting the model object
  modelA = genai.GenerativeModel("gemini-2.0-flash-exp")
  modelB = genai.GenerativeModel("gemini-1.5-flash")
  
  # print('----')
  return modelA, modelB
    
modelA, modelB = set_AI()