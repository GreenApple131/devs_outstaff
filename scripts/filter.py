# filter(func, iterable)

def has_o(string):
    return 'o' in string.lower()

l = ['One', 'two', 'three', '1213fdsffFAS231sdf']


nl = list(filter(has_o, l))
# print(nl)


newl = list(filter(lambda string: 'o' in string.lower(), l))
# print(newl)

newl2 = [string for string in l if has_o(string)]
print(newl2)