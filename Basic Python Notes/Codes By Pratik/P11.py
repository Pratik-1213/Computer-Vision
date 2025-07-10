

# len = len(str)
# new_str = ""
# for i in range(len,0,-1):
#     new_str += str[i-1]


# if(str == new_str):
#     print("Palindrome")
# else:
#     print("Not Palindrome")
str = "Mom"
str = str.lower().replace(" ","")
s = str[::-1]

if(str):
    print("Palindrome")
else:
    print("Not Palindrome")