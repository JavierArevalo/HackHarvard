
import pandas as pd
import sys
import os

from Company import Company

#add all relevant firebase characteristics before

def putToDatabase(jsonRes):

    key = str(jsonRes["stock_name"]) + "Final"
    postAttempt = firebase_app.put('/stocksMinervaMVP', str(key), jsonRes)


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
                company.totalSharesInitially, updatedSharesOutstanding, updatedSharesBought
                company.totalAmountRaising, updatedAmountRaised, amountRemainingToRaise,
                updatedInvestors, company.landingPage, company.progressReport, company.additionalInfo
                )

            putToDatabase(companyUpdated)





        #If confirmation code is anything else
        else if (confirmationCode == 0):
            #Or return any other error message to client
            return "Unsuccessful NFT purchase. No update made to company data. "


    def retrieveCompany(self, companyHash):
        #TODO: retrieve company Object from firebase
        return None


