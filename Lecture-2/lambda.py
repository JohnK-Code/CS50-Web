people = [
    {"name": "Hary", "house": "Gryffindor"},
    {"name": "Cho", "house": "Ravenclaw"},
    {"name": "Draco", "house": "Slytherin"}
]

#def f(person):  ### used to sort dict in list
#    return person["name"]
#people.sort(key=f)

people.sort(key=lambda person: person["name"]) # sorts dict in list using lambda
print(people)
