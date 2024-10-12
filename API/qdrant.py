from flask import Blueprint,request
from dotenv import load_dotenv
from langchain_qdrant import Qdrant
from langchain.embeddings import SentenceTransformerEmbeddings
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance
import os

qdrant_url = os.environ.get('QDRANT_URL')
qdrant_key = os.environ.get('QDRANT_KEY')

qdrant_client = QdrantClient(
    url=qdrant_url, 
    api_key=qdrant_key
)

qdrant_api = Blueprint('qdrant_api', __name__)

embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
db = Qdrant(client=qdrant_client, embeddings=embeddings, collection_name="memory")

@qdrant_api.route("/write_qdrant_data", methods=['POST'])
def write_qdrant_data():
    data = request.json
    qdrant_write_content = list(data.get("questions"))
    # for question in data.get("questions"):
    #     qdrant_write_keys.append(question)
    #     qdrant_write_content.append(data.get(question))
    metadata = []
    for id in list(data.get("ids")):
        metadata.append({"id":id,"usr":data.get("user")})
    try:
        qdrant = Qdrant.from_texts(
            # array which we want to embed
            qdrant_write_content,
            embeddings,
            url=qdrant_url,
            api_key=qdrant_key,
            prefer_grpc=False,
            collection_name="memory",
            metadatas=metadata,
            distance_func=Distance.COSINE
        )
        return {"success":True,"message":"Successfully written into DB","data":{}}
    except Exception as e:
        return {"success":False,"message":str(e),"data":{}}

@qdrant_api.route("/read_qdrant_data", methods=['GET'])
def read_qdrant_data():
    usr = str(request.args.get('user'))
    try:
        docs = db.similarity_search_with_score(query=" ",filter={"usr":usr})
        response = []
        for doc in docs:
            response.append({doc[0].metadata["id"]:doc[0].page_content})
        print(response)
        return {"success":True,"message":"Successfully read qdrant DB","data":response}
    except Exception as e:
        return {"success":False,"message":str(e),"data":{}}

