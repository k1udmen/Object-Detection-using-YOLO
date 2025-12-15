import datetime




class RequestModel:
    def __init__(self,requestId, appCode=None, selfNo=1,valfQuantity=0,transactionDate=None, isCreated=False, isPrinted=False, status=False ):
        self.requestId=requestId
        self.appCode=appCode
        self.valfQuantity=valfQuantity
        self.transactionDate=transactionDate
        self.isCreated=isCreated
        self.isPrinted=isPrinted
        self.selfNo=selfNo
        self.status=status

