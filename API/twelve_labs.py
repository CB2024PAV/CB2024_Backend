from flask import Blueprint,request
from twelvelabs import TwelveLabs
import requests
import os
import dotenv

twelvelabs_api = Blueprint('twelvelabs_api', __name__)

twelve_api_key = os.environ.get("TWELVE_API_KEY")
client = TwelveLabs(api_key=twelve_api_key)
index = os.environ.get("TWELVE_INDEX")

@twelvelabs_api.route("/search_by_text", methods=['GET'])
def search_by_text():
    query = request.args.get('query')
    search_results = client.search.query(
        index_id=index, 
        query_text=query, 
        options=["visual","conversation"]
    )

    try:
        video_id = search_results.data[0].video_id
    except:
        return {"data":{},"message":{"Error 763"},"success":False}

    if video_id:
        url = "https://api.twelvelabs.io/v1.2/indexes/{}/videos/{}".format(index,video_id)
        print(url)
        headers = {
            "accept": "application/json",
            "Content-Type": "application/json",
            "x-api-key":twelve_api_key
        }
        response = requests.get(url, headers=headers)
        return {"data":response.json()["hls"]["video_url"],"message":{},"success":True}
    
    return {"data":{},"message":{"Error 764"},"success":False}
