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
print(google_api_key)
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash")

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
    # print(output.content)
    return {"success":True,"data":output.content,"message":{}}