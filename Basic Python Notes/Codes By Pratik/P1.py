# dict1={'Google': 1, 'Facebook': 2, 'Microsoft': 3}
# dict2={'GFG': 1, 'Microsoft': 2, 'Youtube': 3}
# dict2.update(dict1)

# for key, values in dict2.items():
#     print (key, values)

# print(dict1)


#Patten
# p = '1'
# q = '0'
# j = 0
# k = 4
# while k >= 1:
#     print(" "*j + (k-1)*(p+q) +p+ " "*j)
#     k = k-1
#     j=j+1

n=8
k = 0
for n in range(n,0,-2):
    print(" "*(k),end="")
    for i in range(1,n):
        if i % 2 != 0:
            print("1",end="")
        else:
            print("0",end="")
    print()
    k=k+1