
from dotenv import load_dotenv

load_dotenv() #load all the environment variables
import os
import google.generativeai as genai

from youtube_transcript_api import YouTubeTranscriptApi

genai.configure(api_key=os.getenv("GOOGLE_API_KEY")) #configure the google credentials
model = genai.GenerativeModel("gemini-pro")
prompt = """You are a Youtube video explainer. You will be taking the transcript text and explain the entire video and providing the entire explanation in points. 
You will also be providing the tags for the video. Please explain the video and provide the tags for the video.
Please provide the explanation of the text given here: """
response = None
#getting the summary based on prompt from google gemini
def generate_gemini_content(transcript_text, prompt):
    global response
    response = model.generate_content(prompt+transcript_text)
    return response.text

def initialize_chat_session():
    conversation_history = []
    print("--------------------Initializing chat session---------------------------")
    global chat_session, transcript_text
    if not conversation_history:
        conversation_history.append({
            "role": "user",
            "parts": [
                {"text": "You are a Youtube video explainer. You will be taking the transcript text and answer the questions based on the text from now on. Here is the transcript text: "+str(transcript_text)}
            ]
        })
        conversation_history.append({
            "role": "model",
            "parts": [
                {"text": "Okay, I will answer the questions based on the text. Please ask the questions."}
            ]
        })
    chat_session = model.start_chat(history=conversation_history)

#getting the transcript data from youtube videos
def extract_transcript_details(youtube_video_url):
    global response, transcript_text
    if response:
        return response.text
    try:
        video_id = youtube_video_url.replace('https://www.youtube.com/watch?v=', '')
        transcript_text = YouTubeTranscriptApi.get_transcript(video_id,languages=['en', 'hi'], preserve_formatting=True)
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        for transcript in transcript_list:
            if transcript.language_code == 'en':
                transcript_text = transcript.fetch()
            else:
                transcript_text = transcript.translate('en').fetch()
        transcript=''  
        for i in transcript_text:
            transcript += " "+i['text']
        initialize_chat_session()
        return generate_gemini_content(transcript, prompt) if transcript else 'Transcript not available for this video'

    except Exception as e:
        raise e
    

def start_conversation(message):     
    global chat_session   
    chat_session.send_message(message)
    print(chat_session.history[2:])
    return chat_session.history