class livedb:
    def __init__(self):
        self.data = ["default"]
    def about(self):
        print("the values in index 0 of the database is 'default'.\n please do not change it.\ndata in the database is stored in self.data\n")
    def newrow(self,ipt):
        self.data.append(ipt)
    def showdb(self):
        print(self.data)

#example databases
edb = livedb()
edb.newrow("cloudhub")
edb.showdb()