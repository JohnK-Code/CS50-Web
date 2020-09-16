# examples of python sequances and how to access and alter them

### String = sequance of letters
name = "Harry"
print(name[0])

### List = mutable values - can be changed
names = ["Harry", "Ron", "Hermoine"]
names.append("Draco")
names.sort()
print(names)

### Tuple = immutable values - can't be changed
coordinate = (10.0, 20.0)
print(coordinate)

### Set = unordered unique values - can't add same value twice
s = set()
s.add(1)
s.add(2)
s.add(3)
s.add(4)
s.add(3)
print(s) # Will only print {1,2,3,4}, won't repeat numbers
s.remove(2)
print(s) # Prints {1,3,4}
print(f"The set has {len(s)} elements.") # uses a formatted string literal to print the lengh of set (amount of elements in set)

### Dict = key-value pairs
thisdict = {  # creates dictionary
    "brand": "Ford",
    "model": "Mustang",
    "year": "1964"
}
print(thisdict) # print entire dictionary
x = thisdict["model"] # assigns value of "thisdict" dictionary key called model to variable x
print(x) # prints value of x (key = model in thisdict) from above 
y = thisdict.get("model") # does the same as above, assigns value of key from the thisdict dictonary to y varible - uses get get method this time instead of bracket notation
print(y)
thisdict["year"] = 2018 # changes value of the value assigned to the "year" key in the thisdict dictionary 
print(thisdict) # show change from above