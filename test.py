# for i in range (4,-1,-1):
#     print(i)
print(type('sta'))
ilin = [6, "sav", 46]
s = "hap"
a = ['bob']
for i in range (len(ilin)-1,-1,-1):
    if str(type(ilin[i])) == "<class 'int'>":
        print('int')
    elif str(type(ilin[i])) == "<class 'str'>":
        print("str")
