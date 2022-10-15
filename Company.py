
#Assumptions:
#Can only buy entire NFTs/shares at a time. No percentage or fraction of a share/NFT

import json

class Company:

    def __init__(self, name, valuation, percentEquity, totalSharesInitially,
        sharesOutstanding, sharesBought, totalAmountRaising, amountRaised,
        amountRemainingToRaise, investors, landingPage, progressReport,
        additionalInfo):
        self.name = name
        self.valuation = valuation
        self.percentEquity = percentEquity
        self.totalSharesInitially = totalSharesInitially
        self.sharesOutstanding = sharesOutstanding
        self.sharesBought = sharesBought
        self.totalAmountRaising = totalAmountRaising
        self.amountRaised = amountRaised
        self.amountRemainingToRaise = amountRemainingToRaise
        self.investors = investors
        self.landingPage = landingPage
        self.progressReport = progressReport
        self.additionalInfo = additionalInfo

    def getJSON(self):
        listInvestors = json.dumps(self.investors)
        jsonObject = {
            "name": str(self.name),
            "valuation": float(self.valuation),
            "percentEquity": float(self.percentEquity),
            "totalSharesInitially": int(self.totalSharesInitially),
            "sharesOutstanding": int(self.sharesOutstanding),
            "sharesBought": int(self.sharesBought),
            "totalAmountRaising": float(self.totalAmountRaising),
            "amountRaised": float(self.amountRaised),
            "amountRemainingToRaise": float(self.amountRemainingToRaise),
            "investors": listInvestors,
            "landingPage": str(self.landingPage)
            #Do not include progress report and additional info for now
        }
        return jsonObject
