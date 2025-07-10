# for i in range(1,5):
#     for j in range(1,i+1):
#         print(j,end=" ")
#     print()

# a=2
# for i in range(1,6,2):
#     for j in range(i):
#         print(a,end="\t")
#         a+=2
#     print()


# s = {1,2,3,4,5}

# print(s)
# s.add(6)
# print(s)

# t = (1,2,3,4,5)
# print(t[1:3])
# print(t[1:4])

# def list_Prime(u,l):
#     for num in range(u,l+1):
#         if num > 1:
#             for i in range(2, num):
#               if(num%i)==0:
#                     break
#             else:
#                print(num)
        

# print("\t\t Program to find the list of prime numbers from given range.")

# list_Prime(1,20)


import numpy as np

random_array = np.random.randint(10,20,size=4)
print