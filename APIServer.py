
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
ref = db.reference('/')

firebase_app = firebase.FirebaseApplication('https://hackharvard-ba0b8.firebaseio.com/', None)

#print(ref.get())

#add all relevant firebase characteristics before


#def postToDatabaseOW(json):
    #print("JSON:")
    #print(json)
    #ref = db.reference("/Companies")
    #ref.push()
    #ref.push().set(json)

    #db.collection('App').document('Companies').set(json)

#def postToDatabase(jsonRes):
    #print(firebase_app)
    #postAttempt = firebase_app.post('/companies', jsonRes)
    #print("")
    #print("Post: ")
    #print(postAttempt)
    #print("")
    #return postAttempt

def putToDatabaseCompany(jsonRes, key):

    #key = str(jsonRes["stock_name"]) + "Final"
    puttAttempt = firebase_app.put('/companies', str(key), jsonRes)
    print("")
    print(puttAttempt)
    print("")

def putToDatabaseInvestor(jsonRes, key):
    putAttempt = firebase_app.put('/investors', str(key), jsonRes)
    print("")
    print(putAttempt)
    print("")

def getCompanies():
    data = firebase_app.get('/companies', '')
    return data

def getCompany(key):
    path = '/companies/' + str(key)

    data = firebase_app.get(path, '')
    print("")
    print("Company Retrieved: ")
    print("")
    return data

def getInvestor(key):
    path = '/investors/' + str(key)
    data = firebase_app.get(path, '')
    print("")
    print("Investor Retrieved: ")
    print("")
    print(data)
    return data


class APIServer:

    def __init__(self):
        #Just for logging purposes
        self.numCalls = 0

    def getCompanies(self):
        data = getCompanies()
        return data

    def getCompany(self, companyKey):
        data = getCompany(companyKey)
        return data

    def getInvestor(self, investorKey):
        data = getInvestor(investorKey)
        return data

    def updateInvestorInfo(self, confirmationCode, numSharesBought, dollarAmount, investorKey, companyKey):

        if (confirmationCode == 1):

            #Step 1: retrieve user from firebase using key
            investor = self.getInvestor(investorKey)

            #Investor portfolio:
            #companiesinvested = {'Company A key': 'X shares worth Y', 'Company B key': 'X2 shares worth Y2'}
            #currentDollarPortfolio = investor.dollarPortfolio
            #key = str(companyKey)
            #if key in currentDollarPortfolio:

            #currentDollarPortfolio[str(companyKey)] = (str(numSharesBought) + " shares bought worth " + str(dollarAmount) + " dollars.")

            #Update total number of shares he owns in our platform
            currentNumberSharesOwned = investor.sharesOwn
            updatedSharesOwn = currentNumberSharesOwned + numSharesBought

            #Update total dollar amount invested in our platform
            dollarsInvestedSoFar = investor.dollarsInvested
            updatedDollarsInvested = dollarsInvestedSoFar + dollarAmount

            #update share holdings of each company
            #companyHoldings: {Company A: X shares, Company B: Y shares}
            companyHoldings = investor.companyHoldings

            key = str(companyKey)
            currentCompanyHoldings = 0
            if key in companyHoldings:
                currentCompanyHoldings = companyHoldings[key]
            companyHoldings[key] = numSharesBought + currentCompanyHoldings

            #Create new investor object
            investorUpdated = Investor(investorKey, updatedSharesOwn, dollarsInvestedSoFar, companyHoldings)
            putToDatabaseInvestor(investorUpdated)

        return None

    def updateCompanyInfo(self, confirmationCode, numSharesBought, dollarAmount, hashInvestor, companyKey):

        #Codes:
        #1: Successful NFT Purchase
        #0: Unsuccessful NFT Purchase
        #Anything else: unknown error (HTTP probably)

        #If NFT Purchase successful, do the following:

        if (confirmationCode == 1):

            #Step 1: retrieve company from firebase using hash
            company = getCompany(companyKey)

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

            putToDatabaseCompany(companyUpdated)

            return 200





        #If confirmation code is anything else
        elif (confirmationCode == 0):
            #Or return any other error message to client
            print("Unsuccessful NFT purchase. No update made to company data. ")
            return 404


    def retrieveCompany(self, companyHash):

        #TODO: retrieve company Object from firebase

        return None

if __name__ == "__main__":

    _apiServer = APIServer()
    _companyMinerva = Company("Minerva", 5000000, 10, 100, 100, 0, 500000, 0, 500000, ["Kyle Berg, Chris Klaus"], "https://minerva-landing-6410d.web.app/", None, None)
    #print("here")
    companyJSONMinerva = _companyMinerva.getJSON()
    resMinerva = putToDatabaseCompany(companyJSONMinerva, "minervaHash")


    _companyBuble = Company("Bubbl", 5000000, 8, 200, 180, 20, 400000, 40000, 160000, ["Neo"], "https://linktr.ee/usebubbl?utm_source=linktree_profile_share&ltsid=e144875f-4359-45fb-b3b5-677b16c82e14", None, None)
    companyJSONBuble = _companyBuble.getJSON()
    resBuble = putToDatabaseCompany(companyJSONBuble, "bubleHash")

    _companyCruise = Company("Cruise", 10000000, 5, 500, 50, 450, 500000, 450000, 50000, ["Y Combinator"], "https://getcruise.com/", None, None)
    companyJSONCruise = _companyCruise.getJSON()
    resCruise = putToDatabaseCompany(companyJSONCruise, "cruiseHash")


    #res = putToDatabase(companyJSON, "MinervaHash")

    #retrieve data
    dataMinerva = _apiServer.getCompany("minervaHash")
    print("Data Retrieved for Minerva")
    print(dataMinerva)
    print("")

    dataBuble = getCompany("bubleHash")
    print("Data Retrieved for Buble")
    print(dataBuble)

    dataCruise = getCompany("cruiseHash")
    print("Data Retrieved for Cruise")
    print(dataCruise)

    print("")
    print("Done")
    print("")

    #All companies
    dataCompanies = _apiServer.getCompanies()
    print("Data of all companies")
    print(dataCompanies)
    print("")

    print("Investor")
    investor = {
        "key": "Javi",
        "sharesOwn": 0,
        "dollarsInvested": 0,
        "companyHoldings": {
            "no companies so far": 0,
        }
    }

    putToDatabaseInvestor(investor, "Javi")

    dataInvestor = _apiServer.getInvestor("Javi")
    print("Data Investor")
    print(dataInvestor)

    #print(res)
    #print("Success?")

