# else clause

for i in range(5):
    if i == 6:
        print(i)
        break
# if break activates this else doesn't work
else:
    print('The end')



# else condition is equivalent to this >
flag = False
for i in range(5):
    if i == 6:
        flag = True
        break
if flag:
    print('Smth was found')