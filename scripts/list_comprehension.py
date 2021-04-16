

jack = {
    'name': 'Jack',
    'car': 'Audi'
}

john = {
    'name': 'John',
    'car': 'Opel'
}

users = [jack, john] # list of dictionaries

#list comprehension
cars = [person.get('car', '') for person in users]
print(cars)