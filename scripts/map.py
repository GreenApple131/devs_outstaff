

def upper(string):
    return string.upper()


l = ['one', 'two', 'three']


new_list = list(map(upper, l))
# print(new_list)


new_l = list(map(lambda string: string.upper(), l))
# print(new_l)


# identical result with list comprehension
nl = [string.upper() for string in l]
# print(nl)