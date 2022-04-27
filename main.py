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
    while n < (len(code) - 1):
        line = code[n].split()
        if line[-1] != ";":
            print("Line " + str(n) + " Error: Doesn’t end with semicolon")

        elif line[0] == "int":
            i = 1
            while i < len(line) - 1:
                if (line[i] != "=" or line[i] != "+" or line[i] != "," or line[i] != ";") and \
                        (line[i + 1] != "=" and line[i + 1] != "+" and line[i + 1] != "," and line[i + 1] != ";"):
                    print("Line " + str(n) + " Error: Variable names can’t contain space")
                    break
                elif (line[i] == "=") and \
                        (line[i + 1] == "=" or line[i + 1] == "+" or line[i + 1] == "," or line[i + 1] == ";"):
                    print("Line " + str(n) + " Error: Need value after assignment operator")
                    break
                elif (line[i] != "=" and line[i] != "+" and line[i] != "," and line[i] != ";") and \
                        (line[i + 1] != "=" and line[i + 1] != "+" and line[i + 1] != "," and line[i + 1] != ";"):
                    print("Line " + str(n) + " Error: Need operator between values")
                    break
                else:
                    i += 1
        else:
            i = 0
            if line[0] == "=":
                print("Line " + str(n) + " Error: Missing variable name")

            else:
                while i < len(line) - 1:
                    if line[i] == "+" and (line[i + 1] == "=" or line[i + 1] == "+"
                                           or line[i + 1] == "," or line[i + 1] == ";"):
                        print("Line " + str(n) + " Error: Need value after addition operator")
                        break
                    elif i > 0 and (line[i - 1] == "=" or line[i - 1] == "+" or
                                    line[i - 1] == "," or line[i - 1] == ";") and (line[i] == "+"):
                        print("Line " + str(n) + " Error: Need value before addition operator")
                        break
                    elif (line[i] != "=" and line[i] != "+" and line[i] != "," and line[i] != ";" and
                          line[i] != "return") and (line[i + 1] != "=" and line[i + 1] != "+" and
                                                    line[i + 1] != "," and line[i + 1] != ";"):
                        print("Line " + str(n) + " Error: Illegal type")
                        break
                    elif i > 0 and (line[i - 1] == "=" or line[i - 1] == "+" or line[i - 1] == ","
                                    or line[i - 1] == ";") and (line[i] == "="):
                        print("Line " + str(n) + " Error: Missing variable name")
                    else:
                        i += 1
        n += 1

def CreateSymbolTable(filename):
    # reading the txt file
    f = open(filename, "r")
    code = f.readlines()
    # getting the parameters
    parameters = ParseFunctionHeader(code[0])
    # getting the local variables
    i = 1
    localVar = []
    while i < len(code):
        localVar.extend(ParseLine(code[i]))
        i += 1
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
    return symbolT

def AssemblyGenerator(file):
    symbolT = CreateSymbolTable(file)
    f = open(file, "r")
    code = f.readlines()
    # Split by commas (if there are multiple initializations) and have if statements for each split
    for line in code:
        # splitarray = line.split(",")         #### splits array if there are multiple commas
        # for part in splitarray:              ###
        array=line.split()
        output = []

        for i in range(0, len(array),-1):               ## always have
            if i == len(array) -1:                     # clear register 0 at beginning of line
                output.append("AND R0, R0, 0;")
            if i == 0:
                offset = symbolT[array[i]]
                output.append(WriteVars(offset))

            if str(type(array[i])) == "<class 'int'>":
                output.append(AddNumber(array[i])[0]) # register 0 holds array[:-1]
            elif array[i] == "+":
                print("add")                                           ## is t;his wrong???
            elif array [i] == "=":
                print("equals")
            ##find a way to stop thing
            else: ## just one variable
                offset = symbolT[array[i]]
                output.append(AddVariable(offset))
                print("var add")
            print(output)
        return output





        # for i in range(0, len(array) - 1):
        #     if array[i] == "=":
        #         nvar = array[i - 1]
        #         offset = symbolT[nvar]
        #         value = array[i + 1]
        #         output.append("AND R0, R0, 0;") ## for numberical values
        #         instruction = "ADD R0, R0, "+ str(value) + ";"
        #         output.append(instruction)
        #         instruction = "STR R0, FP," + str(offset) + ";"
        #         output.append(instruction)
        #         output.append(" ")
    #     print(output)
    # return


def AddNumber(num):
    ANout=[]  ## for numberical values
    instruction = "ADD R0, R0, " + str(num) + ";"
    ANout.append(instruction)
    return ANout


def AddVariable(offset):          # loads to R1, adds to R0
    AVout = []
    instruction = "LDR R1, FP," + str(offset) + ";"
    AVout.append(instruction)
    instruction = "ADD R0, R0, R1"
    AVout.append(instruction)
    return AVout


def WriteVars(offset):
    WVout = []
    instruction = "STR R0, FP," + str(offset) + ";"
    WVout.append(instruction)
    return WVout
















if __name__ == '__main__':



    #print(CreateSymbolTable("sample.code"))
    #print(SyntaxCheck("illegal.code"))
    print(AssemblyGenerator("sample.code"))
    '''print(ParseFunctionHeader(str1))
    print(ParseFunctionHeader(str2))
    print(ParseFunctionHeader(str3))
    print(ParseFunctionHeader(str4))
    print(ParseLine(line1))
    print(ParseLine(line2))
    print(ParseLine(line3))
    print(ParseLine(line4))
    print(ParseLine(line5))
    print(ParseLine(line6))
    x = "a b c d e;lkdjfl"
    print(x.split())'''

                # 40184/index.html
                # 43210/choose-db?db=mongo
 #             :30046
#165.106.10.170:50515/index.html
 # 40404/pickDatabase?dbchoice=mongo