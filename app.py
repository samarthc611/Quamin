from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
from bson import ObjectId 

app = Flask(__name__)


client = MongoClient("mongodb+srv://220010052:KC09AxTI9vP555Vh@cluster0.fmo3c2z.mongodb.net/")
db = client.certificates  
collection = db.all_certificates  


@app.route('/verify', methods=['GET'])
def get_info_based_on_id():

    cert_id = request.args.get('cert_id')

    try:
        obj_id = ObjectId(cert_id)
    except Exception as e:
        return jsonify({"error": "Invalid ObjectId format"}), 400

    document = collection.find_one({"_id": obj_id})

    if document:
        document['_id'] = str(document['_id'])
        return render_template('verify.html', cert_id=document['_id'], name=document['name'])
    else:
        return jsonify({"error": "Document not found"}), 404

@app.route('/documents', methods=['GET'])
def get_documents():
    documents = list(collection.find())
    for doc in documents:
        doc['_id'] = str(doc['_id']) 
    return jsonify(documents)

if __name__ == '__main__':
    app.run(debug=True)
