dict1 = {1:"Pratik",2:"Rohit",3:"Saurabh",4:"Shivam",5:"Saurabh"}

# dict1['6'] = "ABC"
# dict1['7'] = "XYZ"
# dict1['8'] = "PQR"


dict2 = {6:"ABC",7:"XYZ",8:"PQR"}
dict1.update(dict2)
print("Dictionary after adding new elements:")
print(dict1)

dict1[2] = "Sherya"
print(dict1)

dict1.pop(1)
print(dict1)
