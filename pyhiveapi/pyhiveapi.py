from datetime import datetime

InitDateTime = None

class Pyhiveapi:
    def __init__(self):
        print("Pyhiveapi __init__")
        InitDateTime = datetime.now()
        self.InitDateTime_self = datetime.now()
        print (str(InitDateTime) + " -- " + str(self.InitDateTime_self))
	
    def GetInitDateTime(self):
        return InitDateTime
	
    def GetInitDateTime_self(self):
        return self.InitDateTime_self

#def main():
#	HiveAPI = Pyhiveapi()