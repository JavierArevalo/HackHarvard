## Mimics a Real World Investor

class Investor:

    ## Investor Level --> can depend on the amountInvestment,income and other factors
    ## TODO: Feature
    def __init__(self, name, email, amtInvestment, walletHash, companyList, investorLevel):
        self.__init__(self, name, email, amtInvestment ,walletHash, companyList)
        self.investorLevel = investorLevel

    ## Default constructor to construct an Investor
    def __init__(self, name, email, amtInvestment, walletHash, companyList):
        self.name = name
        self.email = email
        self.amtInvestment = amtInvestment
        self.investorHash = hash(email)
        self.walletHash = walletHash
        self.companyList = companyList


    ## Differentiating investors basis unique emailId

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.email == other.email

    def __hash__(self):
        return hash(self.email)
