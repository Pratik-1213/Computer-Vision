def interchange_tuples(tup1, tup2): 
    new_tup1 = tup2
    new_tup2 = tup1
    return new_tup1, new_tup2

# Input two tuples
tuple1 = tuple(input("Enter the elements of the first tuple (separated by commas):").split(","))
tuple2 = tuple(input("Enter the elements of the second tuple (separated by commas):").split(","))
# Interchange the tuples
result_tuple1, result_tuple2 = interchange_tuples(tuple1, tuple2)
# Display the result
print("Interchanged tuples:")
print("Tuple 1:", result_tuple1)
print("Tuple 2:", result_tuple2)
