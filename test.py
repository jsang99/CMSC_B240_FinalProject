# for i in range (4,-1,-1):
#     print(i)


#
# print(type('sta'))
# ilin = [6, "sav", 46]
# s = "hap"
# a = ['bob']
# for i in range (len(ilin)-1,-1,-1):
#     if str(type(ilin[i])) == "<class 'int'>":
#         print('int')
#     elif str(type(ilin[i])) == "<class 'str'>":
#         print("str")

#
# adra=["763", "-15"]
# for i in adra:
#     if i.isdigit():
#         i = int(i)
#         print(i)
#
# hap="763"
# ne = "-15"
#
# print(ne.isdigit())
# print(hap.isdigit())





s = '951'
isInt = True
try:
   # converting to integer
   int(s)
except ValueError:
   isInt = False
if isInt:
   print('Input value is an integer')
else:
   print('Not an integer')