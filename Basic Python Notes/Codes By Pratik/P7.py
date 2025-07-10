'''n = int(input("Enter the List Length: "))
list = []
for i in range(n):
    list.append(int(input("Enter the List Element: ")))

print("List: ", max(list))
print("List: ", min(list))'''

class Student:

    def __init__(self):
        self.name = ""
        self.rollno = 0
        self.depertment = ""
        self.mobileno = 0
        
    def getdata(self):
        self.name = input("Enter the name: ")
        self.rollno = int(input("Enter the roll no: "))
        self.depertment = input("Enter the department: ")
        self.mobileno = int(input("Enter the mobile no: "))

    def putdata(self):
        print("Name: ", self.name)
        print("Roll No: ", self.rollno)
        print("Department: ", self.depertment)
        print("Mobile No: ", self.mobileno)

s = Student()
s.getdata()
s.putdata()