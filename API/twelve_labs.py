from flask import Blueprint,request
from twelvelabs import TwelveLabs
import requests
import os
import dotenv

twelvelabs_api = Blueprint('twelvelabs_api', __name__)

twelve_api_key = os.environ.get("TWELVE_API_KEY")
client = TwelveLabs(api_key=twelve_api_key)
index = os.environ.get("TWELVE_INDEX")

def get_video_url(video_id):
    url = "https://api.twelvelabs.io/v1.2/indexes/{}/videos/{}".format(index,video_id)
    print(url)
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
        "x-api-key":twelve_api_key
    }
    response = requests.get(url, headers=headers)
    return response.json()["hls"]["video_url"]

@twelvelabs_api.route("/search_by_text", methods=['GET'])
def search_by_text():
    query = request.args.get('query')
    print(query)
    search_results = client.search.query(
        index_id=index, 
        query_text=query, 
        options=["visual","conversation"]
    )

    try:
        video_id = search_results.data[0].video_id
        if video_id:
            return {"data":get_video_url(video_id),"message":{},"success":True}
    except:
        return {"data":{},"message":{"Error 763"},"success":False}
    
    return {"data":{},"message":{"Error 764"},"success":False}

@twelvelabs_api.route("/search_by_image", methods=['POST'])
def search_by_image():
    if 'image' not in request.files:
        return {"data":{},"message":{"Error 765"},"success":False}
    
    image = request.files['image']
    image.save('./image.jpg')

    search_results = client.search.query(
        index_id=index,
        query_media_type="image",
        query_media_file="./image.jpg", 
        options=["visual"]
    )

    try:
        video_id = search_results.data[0].video_id
        if video_id:
            return {"data":get_video_url(video_id),"message":{},"success":True}
    except:
        return {"data":{},"message":{"Error 766"},"success":False}
    finally:
        os.remove("./image.jpg")
    
    return {"data":{},"message":{"Error 767"},"success":False}