# test strings
str1 = "int fun0 ( ) {"
str2 = "int fun1 ( int a ) {"
str3 = "int fun2 ( int dog , int cat ) {"
str4 = "int fun3 ( int x , int y , int z ) {"
line1 = "int x ;"
line2 = "int j , k ;"
line3 = "int y = 2 ;"
line4 = "int a = x + 5 ;"
line5 = "int b = a + y + 8 ;"
line6 = "int c = a + x , d , e = b ;"


def ParseFunctionHeader(str):
    argument=str.split("(")[1].split(")")[:-1][0].replace("int","").replace(",","")
    print(argument.split())

def ParseLine(line):
    print(line.split(","))


if __name__ == '__main__':
    #ParseFunctionHeader(str1)
    #ParseFunctionHeader(str2)
    #ParseFunctionHeader(str3)
    #ParseFunctionHeader(str4)
    ParseLine(line1)
    ParseLine(line2)
    ParseLine(line3)
    ParseLine(line4)
    ParseLine(line5)
    ParseLine(line6)
