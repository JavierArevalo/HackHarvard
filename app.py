# app.py

# Required imports
import os
from flask import Flask, request, jsonify
from firebase_admin import credentials, db, initialize_app

from APIServer import APIServer

# Initialize Flask app
app = Flask(__name__)
_apiServer = APIServer()
# Initialize Firestore DB
#cred = credentials.Certificate('HackHarvardAUTH.json')
#default_app = initialize_app(cred, {
   # 'databaseURL': 'https://hackharvard-ba0b8.firebaseio.com/'
#})
#company_ref = db.reference('/companies')
#investor_ref = db.reference('/investors')

# @app.route('/add', methods=['POST'])
# def create():
#     """
#         create() : Add document to Firestore collection with request body.
#         Ensure you pass a custom ID as part of json body in post request,
#         e.g. json={'id': '1', 'title': 'Write a blog post'}
#     """
#     try:
#         id = request.json['id']
#         company_ref.document(id).set(request.json)
#         return jsonify({"success": True}), 200
#     except Exception as e:
#         return f"An Error Occurred: {e}"

# Currently, in use
@app.route('/getCompany', methods=['GET'])
def readOne():
    companyKey = request.args.get('name')

    dataOne = _apiServer.getCompany(companyKey)
    return dataOne

@app.route('/list', methods=['GET'])
def read():
    data = _apiServer.getCompanies()
    return data
    """
        read() : Fetches documents from Firestore collection as JSON.
        todo : Return document that matches query ID.
        all_todos : Return all documents.
    """
    try:
        # Check if companyName was passed to URL query
        com_nam = request.args.get('name')
        if com_nam:
            company = company_ref.get(com_nam)
            return jsonify(company), 200
        else:
            all_companies = [doc.to_dict() for doc in company_ref.stream()]
            return jsonify(all_companies), 200
    except Exception as e:
        return f"An Error Occurred: {e}"


@app.route('/invest', methods=['POST', 'PUT'])
def invest(json):
    #need json or specific data to update values
    confirmation = json["confirmation"]
    numSharesBought = json["sharesBought"]
    dollarAmount = json["dollarAmount"]
    hashInvestor = json["investorKey"]
    companyKey = json["companyKey"]

    #_apiServer = APIServer()

    updateResponse = _apiServer.updateInvestorInfo(confirmation, numSharesBought, dollarAmount, hashInvestor, companyKey)
    if (updateResponse == 200):
        return 200

    """
        invest() : Invest in the company.
        Does the following things:
        1: Reduce the number of NFTs available from companies
        2: Add the company to the investor's portfolio
        3: Returns success if all the above operations are successful.
        Ensure you pass a custom ID as part of json body in post request,
        e.g. json={'id': '1', 'title': 'Write a blog post today'}
    """
    try:
        id = request.json['id']
        company_ref.document(id).update(request.json)
        return jsonify({"success": True}), 200
    except Exception as e:
        return f"An Error Occurred: {e}"


port = int(os.environ.get('PORT', 8080))
if __name__ == '__main__':
    app.run(threaded=True, host='0.0.0.0', port=port)
