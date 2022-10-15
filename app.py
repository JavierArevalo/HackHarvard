# app.py

# Required imports
import os
from flask import Flask, request, jsonify
from firebase_admin import credentials, db, initialize_app

# Initialize Flask app
app = Flask(__name__)

# Initialize Firestore DB
cred = credentials.Certificate('HackHarvard.json')
default_app = initialize_app(cred, {
    'databaseURL': 'https://hackharvard-ba0b8.firebaseio.com/'
})
company_ref = db.reference('/Companies')


@app.route('/add', methods=['POST'])
def create():
    """
        create() : Add document to Firestore collection with request body.
        Ensure you pass a custom ID as part of json body in post request,
        e.g. json={'id': '1', 'title': 'Write a blog post'}
    """
    try:
        id = request.json['id']
        company_ref.document(id).set(request.json)
        return jsonify({"success": True}), 200
    except Exception as e:
        return f"An Error Occurred: {e}"


@app.route('/list', methods=['GET'])
def read():
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

@app.route('/listAll', methods=['GET'])
def read():
    """
        read() : Fetches documents from Firestore collection as JSON.
        todo : Return document that matches query ID.
        all_todos : Return all documents.
    """
    try:
        # Check if companyName was passed to URL query
        com_nam = request.args.get()
        if com_nam:
            company = company_ref.get(com_nam)
            return jsonify(company), 200
        else:
            all_companies = [doc.to_dict() for doc in company_ref.stream()]
            return jsonify(all_companies), 200
    except Exception as e:
        return f"An Error Occurred: {e}"


@app.route('/update', methods=['POST', 'PUT'])
def update():
    """
        update() : Update document in Firestore collection with request body.
        Ensure you pass a custom ID as part of json body in post request,
        e.g. json={'id': '1', 'title': 'Write a blog post today'}
    """
    try:
        id = request.json['id']
        company_ref.document(id).update(request.json)
        return jsonify({"success": True}), 200
    except Exception as e:
        return f"An Error Occurred: {e}"


@app.route('/delete', methods=['GET', 'DELETE'])
def delete():
    """
        delete() : Delete a document from Firestore collection.
    """
    try:
        # Check for ID in URL query
        todo_id = request.args.get('id')
        company_ref.document(todo_id).delete()
        return jsonify({"success": True}), 200
    except Exception as e:
        return f"An Error Occurred: {e}"


port = int(os.environ.get('PORT', 8080))
if __name__ == '__main__':
    app.run(threaded=True, host='0.0.0.0', port=port)
