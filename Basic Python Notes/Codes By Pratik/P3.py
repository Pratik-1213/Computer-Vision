class Diploma:
    def getDiploma(self):
        print("I Got a Diploma")

class Co(Diploma):
    def getDiploma(self):
        print("I am with Co diploma")

class IF(Diploma):
    def getDiploma(self):
        print("I am with IF diploma")

d = Diploma()
c = Co()
i = IF()

d.getDiploma()

c.getDiploma()

i.getDiploma()

