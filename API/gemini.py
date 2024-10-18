from flask import Blueprint,request
import google.generativeai as genai
from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from API.qdrant import read_qdrant_data
from datetime import datetime
from dotenv import load_dotenv
import os

# from google.cloud import texttospeech
# import base64
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

gemini_api = Blueprint('gemini_api', __name__)

google_api_key = os.environ.get("GOOGLE_API_KEY")
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash")

# os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "/home/prathik/git/cerebral-hack/CB2024_Backend/API/gcpconfig.json"
# client = texttospeech.TextToSpeechClient()


# def text_to_speech(input_text):
#     synthesis_input = texttospeech.SynthesisInput(text=input_text)
    
#     voice = texttospeech.VoiceSelectionParams(language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL)
#     audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)
    
#     response = client.synthesize_speech(input=synthesis_input, voice=voice, audio_config=audio_config)
    
#     audio_content_base64 = base64.b64encode(response.audio_content).decode('utf-8')
#     url = f"data:audio/mp3;base64,{audio_content_base64}"
#     return url


def get_chat_response(background, question):
    dt = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    chat_prompt = PromptTemplate(
        input_variables=["background", "question", "date"],
        template="""
        You are like a personal assistant to a person who has a type of memory impairment. Some relevant background information about the patient is as follows.
        
        {background}
        
        Given the above background and context answer the below question. Look for any additional details you need. 
        Adapt your tone of talking according to the end user.
        Something you might need to know is today's date is {date}. 
        
        {question}
        
        Guidelines for Talking to Individuals with Memory Impairments:
        1. ALWAYS rely on the information I provide to you. Ensure all responses are fact-based, validated, and avoid hallucinations. Do not provide any unknown, unvalidated, or potentially unsafe information. 
        2. Use simple language and short sentences. Avoid complex words.
        3. Focus on the present. Avoid relying on past memories.
        4. Offer gentle reassurance and avoid correcting memory lapses.
        5. Stick to familiar routines and give clear, one-step instructions.
        6. Pair words with visual or physical cues when possible.
        7. Ask one question at a time, offering yes/no or simple choices.
        8. Keep the tone positive, compassionate, and patient, even if repeating answers.
        9. Encourage engagement without pressure or expectation of recall.
        """
    )

    output_int = llm.invoke(chat_prompt.format(background = background, question=question, date=dt))

    final_prompt = PromptTemplate(
        input_variables=["answer", "question"],
        template="""
        

        Question: {question}
        Answer: {answer}
        
        The answer may or may not be an elaborated version with extra explanation. Can you understand the question and answer and only pick out the main points needed. 
        You are like a personal assistant to a person who has a type of memory impairment. Adapt your tone of talking according to the end user and avoid talking in third person.
        Give me ONLY the answer.
        """
    )

    output = llm.invoke(final_prompt.format(question=question, answer = output_int))
    return output.content

@gemini_api.route("/get_good_morning_msg", methods=['GET'])
def get_good_morning_msg():
    usr = str(request.args.get('user'))
    dt = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    background = ""
    for text in read_qdrant_data(usr)["data"]:
        background += " " + list(text.values())[0]

    good_morning = PromptTemplate(
        input_variables=["background", "date"],
        template="""
        Generate a good morning message for a patient who is having a kind memory impairment.
        The message should include a pleasant greeting, today's date, brief about who he is, past key events, goals for the day, a breif health and wellness check and an encouraging note in the end.
        Below are details about the patient that can help you formulate a nice paragraph in not more than 200 words.
        Some Details you might need to respond would be the time of the day: {date}
        Use a kind normal human like tone
        {background}
        
        Guidelines for Talking to Individuals with Memory Impairments:
        1. ALWAYS rely on the information I provide to you. Ensure all responses are fact-based, validated, and avoid hallucinations. Do not provide any unknown, unvalidated, or potentially unsafe information. 
        2. Take into consideration the time of the day, season, safety aspects of the responses.
        3. Use simple language and short sentences. Avoid complex words.
        4. Focus on the present. Avoid relying on past memories.
        5. Offer gentle reassurance and avoid correcting memory lapses.
        6. Stick to familiar routines and give clear, one-step instructions.
        7. Pair words with visual or physical cues when possible.
        8. Ask one question at a time, offering yes/no or simple choices.
        9. Keep the tone positive, compassionate, and patient, even if repeating answers.
        10. Encourage engagement without pressure or expectation of recall."""
    )

    output = llm.invoke(good_morning.format(background = background, date=dt))
    # url = text_to_speech(output.content)

    return {
        "success":True, 
        "data":output.content, 
        # "video": url, 
        "message":{}
        }

@gemini_api.route("/get_reply", methods=['GET'])
def get_reply():
    usr = str(request.args.get('user'))
    question = str(request.args.get('query'))
    background = ""
    for text in read_qdrant_data(usr,question,k=4)["data"]:
        background += " " + list(text.values())[0]

    response = get_chat_response(background,question)
    # url = text_to_speech(response)
    return {
        "success":True,
        "data":response, 
        # "video": url,
        "message":{}
    }