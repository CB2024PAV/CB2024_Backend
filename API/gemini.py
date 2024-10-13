from flask import Blueprint,request
from dotenv import load_dotenv
import os
import google.generativeai as genai
from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from qdrant import read_qdrant_data
from datetime import date

gemini_api = Blueprint('gemini_api', __name__)

google_api_key = os.environ.get("GOOGLE_API_KEY")
load_dotenv()
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash")

def get_chat_response(background, question):
    dt = date.today()

    chat_prompt = PromptTemplate(
        input_variables=["background", "question"],
        template="""
        {background}
        
        Given the above background and context answer the below question. Look for any additional details you need. 
        Something you might need to know is today's date is {date}. 
        
        {question}"""
    )

    output_int = llm.invoke(chat_prompt.format(background = background, question=question, date=dt))

    final_prompt = PromptTemplate(
        input_variables=["answer", "question"],
        template="""
        Question: {question}
        Answer: {answer}
        
        The answer may or may not be an elaborated version with extra explanation. Can you understand the question and answer and only pick out the main points needed. 
        Give me ONLY the answer.
        """
    )

    output = llm.invoke(final_prompt.format(question=question, answer = output_int))
    return output.content

@gemini_api.route("/get_good_morning_msg", methods=['GET'])
def get_good_morning_msg():
    usr = str(request.args.get('user'))
    background = ""
    for text in read_qdrant_data(usr)["data"]:
        background += " " + list(text.values())[0]

    good_morning = PromptTemplate(
        input_variables=["background"],
        template="""
        Generate a good morning message for a patient who is having a kind memory impairment.
        The message should include a pleasant greeting, today's date, brief about who he is, past key events, goals for the day, a breif health and wellness check and an encouraging note in the end.
        Below are details about the patient that can help you formulate a nice paragraph in not more than 200 words.
        {background}"""
    )

    output = llm.invoke(good_morning.format(background = background))
    return {"success":True,"data":output.content,"message":{}}

@gemini_api.route("/get_reply", methods=['GET'])
def get_reply():
    usr = str(request.args.get('user'))
    question = str(request.args.get('query'))
    background = ""
    for text in read_qdrant_data(usr,question,k=4)["data"]:
        background += " " + list(text.values())[0]

    response = get_chat_response(background,question)
    return {"success":True,"data":response,"message":{}}