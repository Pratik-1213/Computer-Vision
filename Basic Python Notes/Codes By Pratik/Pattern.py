# for i in range(5,0,-1):
#     for j in range(1,i+1):
#         print("*", end="")
#     print()

# for i in range(5,0,-1):
#     print("* " * i)


# arr = [1,2,3,4,5]
# print(arr.__len__())
# print(len(arr))

# l = [1,2,3,4,5]
# l.append(6)
# print(l)


# s1= {1,2,3,4,5}
# s2= {4,5,6,7,8}

# print(s1 ^ s2)

# x = lambda a,b,c,d: a+b+c+d
# print(x(1,2,3,4))


# x = lambda a: a**0.5
# print(x(16))

import collections
import pprint
file_input = input('File Name: ')
with open(file_input, 'r') as info:
    # Read the file and count the occurrences of each character
    # Convert to uppercase to ignore case
     # Use collections.Counter to count occurrences
     # Use pprint to format the output
 count = collections.Counter(info.read().upper())
 value = pprint.pformat(count)
print(value)