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
    argument = str.split("(")[1].split(")")[:-1][0].replace("int", "").replace(",", "")
    return argument.split()


def ParseLine(line):
    array = line.split()
    i = 1
    variables = []
    while i < len(array) - 1:
        if array[i - 1] == 'int' or array[i - 1] == ',':
            variables.append(array[i])
        i += 1
    return variables


def SyntaxCheck(filename):
    f = open(filename, "r")
    code = f.readlines()
    n = 1
    for n in range(len(code)):
        n += 1
        print("new line", n)
        line = code[n].split()
        #print(line)
        #print(len(line))
        if line[-1] != ";":
            print("Line " + str(n) + " Error: Doesn’t end with semicolon")
            n+=1
        elif line[0] == "int":
            i = 1
            while i < len(line) - 1:
                if (line[i] != "=" or line[i] != "+" or line[i] != "," or line[i] != ";") and \
                        (line[i + 1] != "=" and line[i + 1] != "+" and line[i + 1] != "," and line[i + 1] != ";"):
                    print("Line " + str(n) + " Error: Variable names can’t contain space")
                    print(line[i], (line[i+1]))
                    i += 1
                else:
                    break
            n+=1




def CreateSymbolTable(filename):
    # reading the txt file
    f = open(filename, "r")
    code = f.readlines()
    # getting the parameters
    parameters = ParseFunctionHeader(code[0])
    # print(parameters)
    # getting the local variables
    i = 1
    localVar = []
    while i < len(code):
        localVar.extend(ParseLine(code[i]))
        i += 1
    # print(localVar)
    # assigning offset
    symbolT = {}
    counter = 0
    for lv in localVar:
        symbolT[lv] = counter
        counter -= 1
    counter = 4
    for p in parameters:
        symbolT[p] = counter
        counter += 1
    print(symbolT)


if __name__ == '__main__':
    # CreateSymbolTable("sample.code")
    print(SyntaxCheck("illegal.code"))

    '''print(ParseFunctionHeader(str1))
    print(ParseFunctionHeader(str2))
    print(ParseFunctionHeader(str3))
    print(ParseFunctionHeader(str4))
    print(ParseLine(line1))
    print(ParseLine(line2))
    print(ParseLine(line3))
    print(ParseLine(line4))
    print(ParseLine(line5))
    print(ParseLine(line6))'''
