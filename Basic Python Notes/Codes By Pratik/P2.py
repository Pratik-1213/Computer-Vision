# def check_palindrome(n):
#     num = n
#     rev=0
#     rem=0
#     while n > 0:
#         rem = n % 10
#         rev = rev * 10 + rem
#         n = n // 10

#     return num == rev

# n = int(input("Enter a number: "))
# if check_palindrome(n):
#     print(f"{n} is a palindrome")
# else:
#     print(f"{n} is not a palindrome")


#Write a python program to create a user defined module that will ask your program name and display the name of the program.

# import mod1

# str = input("Enter the program name: ")
# mod1.pro_name(str)

import numpy as np

random_int = np.random.randint(10,50,size=5)
print("Random Integer: ", random_int)