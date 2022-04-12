# test strings
str1 = "int fun0 ( ) {"
str2 = "int fun1 ( int a ) {"
str3 = "int fun2 ( int dog , int cat ) {"
str4 = "int fun3 ( int x , int y , int z ) {"


def ParseFunctionHeader(str):
    argument=str.split("(")[1].split(")")[:-1][0].replace("int","").replace(",","")
    print(argument.split())
if __name__ == '__main__':
    ParseFunctionHeader(str1)
    ParseFunctionHeader(str2)
    ParseFunctionHeader(str3)
    ParseFunctionHeader(str4)
