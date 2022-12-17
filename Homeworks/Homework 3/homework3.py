# Homework 3

# Question 1
"""
from functools import reduce 

def convert_to_decimal(bits):
    exponents = range(len(bits)-1, -1, -1)
    nums = [2**x[1] if x[0] == 1 else 0 for x in zip(bits, exponents)] 
    return reduce(lambda acc, num: acc + num, nums)

"""

# Question 2
# part a 
"""
def parse_csv(lines): 
    tupleList = [(str(x.split(",")[0]), int(x.split(",")[1])) for x in lines]
    return tupleList

print(parse_csv(["apple,8", "pear,24", "gooseberry,-2"])) #should return [("apple", 8), ("pear", 24), ("gooseberry", -2)].
"""

"""
lines = ["apple,8", "pear,24", "gooseberry,-2"]
x, y, z = lines
print(x)
print(y)
print(z)
words = x.split(',')
print(words)
"""


# Question 2
# part b 
"""
def unique_characters(sentence): 
    return {s for s in sentence}

print(unique_characters("happy")) # should return {"h", "a", "p", "y"}.)
"""
    
"""
# Question 2
# part c 
def squares_dict(lower_bound, upper_bound): 
    dict = {i:i**2 for i in range(lower_bound, upper_bound + 1)}
    return dict

print(squares_dict(1, 5)) # should return {1: 1, 2: 4, 3: 9, 4: 16, 5: 25}.
"""

# Question 3
def strip_characters(sentence, chars_to_remove):
    return "".join(filter(lambda x: sentence[x:] in chars_to_remove, sentence))

print(strip_characters("Hello, world!", {"o", "h", "l"})) # should return "He, wrd!"

# Question 4
