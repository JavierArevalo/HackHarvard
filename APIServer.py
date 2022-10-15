
import pandas as pd
import sys
import os

import json

from jsonmerge import merge

#firebase
import firebase_admin
from firebase_admin import credentials, firestore
from firebase_admin import db
from google.cloud import storage

from firebase import firebase

storage_client = storage.Client()


#firebaseConfig = credentials.Certificate('./HackHarvardAUTH.json')

#default_app = firebase_admin.initialize_app(firebaseConfig)

#db = firestore.client()

#fb = firebase.FirebaseApplication('https://hackharvard-ba0b8-default-rtdb.firebaseio.com/', None)

#cred = credentials.Certificate('HackHarvardAUTH.json')
#cred = credentials.ApplicationDefault()
#ef = db.reference('/')
from Company import Company


#Old way
cred_path = os.path.join(os.getcwd(), "HackHarvardAUTH.json")
cred = credentials.Certificate(cred_path)
#cred = credentials.ApplicationDefault()
app = firebase_admin.initialize_app(cred, {'databaseURL': 'https://hackharvard-ba0b8.firebaseio.com/'})

#ref = db.reference('/')
#print(ref.get())
#print("Trial")

firebase_app = firebase.FirebaseApplication('https://hackharvard-ba0b8.firebaseio.com/', None)

ref = db.reference('/')
print(ref.get())

#add all relevant firebase characteristics before


def postToDatabaseOW(json):
    print("JSON:")
    print(json)
    ref = db.reference("/Companies")
    ref.push()
    ref.push().set(json)

    #db.collection('App').document('Companies').set(json)

def postToDatabase(jsonRes):
    print(firebase_app)
    postAttempt = firebase_app.post('/companies', jsonRes)
    print("")
    print("Post: ")
    print(postAttempt)
    print("")
    return postAttempt

def putToDatabase(jsonRes, key):

    #key = str(jsonRes["stock_name"]) + "Final"
    puttAttempt = firebase_app.put('/companies', str(key), jsonRes)
    print("")
    print(puttAttempt)
    print("")

def getData():
    data = firebase_app.get('/companies/', '')
    print("")
    print("Data Retrieved: ")
    print("")
    return data


class APIServer:

    def __init__(self):
        #Just for logging purposes
        self.numCalls = 0

    def updateCompanyInfo(self, confirmationCode, numSharesBought, dollarAmount, hashInvestor, hashCompany):

        #Codes:
        #1: Successful NFT Purchase
        #0: Unsuccessful NFT Purchase
        #Anything else: unknown error (HTTP probably)

        #If NFT Purchase successful, do the following:

        if (confirmationCode == 1):

            #Step 1: retrieve company from firebase using hash
            company = self.retrieveCompany(companyHash)

            initialTotalSharesOutstanding = company.initialSharesOutstanding

            #Update shares outstanding
            currentSharesOutstanding = company.sharesOutstanding
            updatedSharesOutstanding = currentSharesOutstanding - numSharesBought

            #Update total number of shares bough so far
            currentSharesBought = company.sharesBought
            updatedSharesBought = currentSharesBought + numSharesBought

            #update amount raised
            currentAmountRaised = company.amountRaised
            updatedAmountRaised = currentAmountRaised + dollarAmount

            #Add current investor
            listCurrentInvestors = company.investors #should return a list
            objectInvestor = {
                "investorHash": str(hashInvestor),
                "numShares": float(numSharesBought),
                "dollarValue": float(dollarAmount)
            }
            updatedInvestors = listCurrentInvestors.append(objectInvestor)

            #Amount remaining to raise
            totalAmountRaising = company.totalAmountRaising
            amountRemainingToRaise = totalAmountRaising - updatedAmountRaised

            #Create new object: not as efficient as updating but works better due to pointers and memory concerns
            #Order:

            #Name
            #Valuation
            #Percent of equity available to investors

            #Total shares initially available
            #Shares outstanding (remaining)
            #Shares Bought

            #Total amount to raise
            #Amount reaised
            #Amount remaining to Raise

            #List of investors

            #Link to landing page
            #Progress report
            #Additional info

            #update with put object (using company hash as key)

            companyUpdated = Company(company.name, company.valuation, company.percentEquity,
                company.totalSharesInitially, updatedSharesOutstanding, updatedSharesBought,
                company.totalAmountRaising, updatedAmountRaised, amountRemainingToRaise,
                updatedInvestors, company.landingPage, company.progressReport, company.additionalInfo
                )

            putToDatabase(companyUpdated)





        #If confirmation code is anything else
        elif (confirmationCode == 0):
            #Or return any other error message to client
            return "Unsuccessful NFT purchase. No update made to company data. "


    def retrieveCompany(self, companyHash):
        #TODO: retrieve company Object from firebase
        return None

if __name__ == "__main__":

    _apiServer = APIServer()
    _company = Company("Minerva", 5000000, 10, 10, 10, 0, 500000, 0, 500000, ["Kyle Berg"], "https://minerva-landing-6410d.web.app/", None, None)
    print("here")
    companyJSON = _company.getJSON()
    print(companyJSON)
    res = postToDatabaseOW(companyJSON)
    #res = putToDatabase(companyJSON, "MinervaHash")

    #retrieve data
    data = getData()
    print("Data Retrieved")
    print(data)
    #print(res)
    #print("Success?")

