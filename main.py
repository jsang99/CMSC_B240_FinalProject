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
        if (array[i - 1] == 'int' or array[i - 1] == ',') and array[i - 1] != "return":
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
    symbolT = CreateSymbolTable(file)  # get symbol table
    # print(symbolT)
    f = open(file, "r")
    code = f.readlines()
    # Split by commas (if there are multiple initializations) and have if statements for each split
    lineNum = 1
    for line in code[1:]:
        print("Line " + str(lineNum))
        print(line)
        # splitarray = line.split(",")         #### splits array if there are multiple commas
        # for part in splitarray:              ###
        array = line.split()
        print(array)
        output = []
        for i in range(len(array) - 1, -1, -1):
            print("type:", type(array[i]))
            print("i =", i)
            print("element:", array[i])

            # array[i] = intChange(array[i])  ## change str to int if possible

            if i == len(array) - 1:
                # clear register 0 at beginning of line
                print("Operation:", 'getting rid of ;')
                output.append("AND R0, R0, 0;")
            elif i == 0 and (array[i] == "int"):
                print("Operation:", 'end')
            elif str(type(array[i])) == "<class 'int'>":
                print('int')
                output.append(AddNumber(array[i])[0])  # register 0 holds array[:-1]
            elif array[i] == "+":
                print("add")  ## is t;his wrong???
            elif array[i] == "=":
                print("equals")
                offset = symbolT[array[i - 1]]
                output.append(WriteVars(offset))
            elif str(type(array[i])) == "<class 'str'>":  ## just one variable
                print('var')
                print()
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
    ANout = []  ## for numberical values
    instruction = "ADD R0, R0, " + str(num) + ";"
    ANout.append(instruction)
    return ANout


def AddVariable(offset):  # loads to R1, adds to R0
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


def intChange(str):
    isInt = True
    try:
        # converting to integer
        int(str)
    except ValueError:
        isInt = False
    if isInt:
        return int(str)






# KEVIN's codes
def AssemblyGeneratorKevin(file):
    symbolT = CreateSymbolTable(file)  # get symbol table
    # print(symbolT)
    f = open(file, "r")
    code = f.readlines()
    parameters = ParseFunctionHeader(code[0])
    allLocalVars = []
    output = []
    for line in code[1:-1]:
        if "," in line:
            newline = "int"+line[line.index(",")+1:]
            code.insert(code.index(line),newline)
            line = line[:line.index(",")]
            #print(newline)
            #print("line changed to :",line)
        array = line.split()
        # print(array)
        if "int" in array and "=" not in array and "+" not in array:
            pass

        if "int" in array and "=" in array and "+" not in array:
            # output = []
            # parsing
            value = array[array.index("=") + 1]
            localVar = array[array.index("int") + 1]
            if localVar not in allLocalVars:
                allLocalVars.append(localVar)
            else:
                return "Error: variable " + localVar + " is being declared a second time."
            offset = str(symbolT[localVar])

            # generating instructions
            instr = "AND R0, R0, 0; clear R0" + "\n"
            output.append(instr)
            instr = "ADD R0, R0, " + value + "; add " + value + " to R0"  + "\n"
            output.append(instr)
            instr = "STR R0, FP, " + offset + "; write " + localVar  + "\n"
            output.append(instr)
            # print(output)

        if "int" in array and "=" in array and "+" in array:
            # output = []
            # parsing
            localVar = array[array.index("int") + 1]
            if localVar not in allLocalVars:
                allLocalVars.append(localVar)
            usedParameters = []
            usedParameterCounter = 0
            regNum = usedParameterCounter
            plusCounter = 0
            plusLocation = []
            for element in array:
                if element == "+":
                    plusCounter += 1
                    plusLocation.append(array.index(element))
            for parameter in parameters:
                if parameter in array:
                    usedParameters.append(parameter)

            # generating instructions
            for element in array[array.index("="):]:
                if element in allLocalVars or usedParameters and element != "=" and element != "+" and element != ";":
                    instr = "LDR R" + str(regNum) + ", FP, " + str(symbolT[element]) + "; read " + element + "\n"
                    output.append(instr)
                    regNum += 1

            i = 0
            for i in range(plusCounter):
                instr = "ADD R0, R" + str(i) + ", R" + str(i + 1) + "; put sum in R0" + "\n"
                output.append(instr)
                i += 1
            instr = "STR R0, FP, " + str(symbolT[localVar]) + "; write " + localVar + "\n"
            output.append(instr)
            # print(output)

        if "int" not in array and "=" in array and "+" in array:
            # output = []
            # parsing
            localVar = array[array.index("=") - 1]
            if localVar not in allLocalVars:
                return "Error: variable " + localVar + " is undeclared."
            usedParameters = []
            usedParameterCounter = 0
            regNum = usedParameterCounter
            plusCounter = 0
            plusLocation = []
            constantLocation = []
            for element in array:
                if element == "+":
                    plusCounter += 1
                    plusLocation.append(array.index(element))
            for parameter in parameters:
                if parameter in array:
                    usedParameters.append(parameter)
            if len(usedParameters) < plusCounter + 1:
                for location in plusLocation:
                    if array[location - 1] not in usedParameters:
                        if array[location - 1] not in allLocalVars and not array[location + 1].isdigit():
                            return "Error: variable " + array[location - 1] + " is undeclared."
                        else:
                            constantLocation.append(location - 1)
                    if array[location + 1] not in usedParameters:
                        constantLocation.append(location + 1)
                        if array[location + 1] not in allLocalVars and not array[location + 1].isdigit():
                            return "Error: variable " + array[location + 1] + " is undeclared."
                        else:
                            constantLocation.append(location + 1)

            # generating instructions
            for usedParameter in usedParameters:
                instr = "LDR R" + str(regNum) + ", FP, " + str(symbolT[usedParameter]) + "; read " + usedParameters[
                    usedParameterCounter] + "\n"
                output.append(instr)
                regNum += 1

            for location in constantLocation:
                instr = "AND R" + str(regNum) + ", R" + str(regNum) + ", 0; clear R" + str(regNum) + "\n"
                output.append(instr)
                instr = "ADD R" + str(regNum) + ", R" + str(regNum) + ", " + str(array[location]) + "; add " + str(
                    array[location]) + " to R" + str(regNum) + "\n"
                output.append(instr)
                regNum += 1

            i = 0
            for i in range(plusCounter):
                instr = "ADD R0, R" + str(i) + ", R" + str(i + 1) + "; put sum in R0" + "\n"
                output.append(instr)
                i += 1
            instr = "STR R0, FP, " + str(symbolT[localVar]) + "; write " + localVar + "\n"
            output.append(instr)

        if "return" in array:
            array = array[1:]
            # parsing
            # localVar = array[array.index("=") - 1]
            # if localVar not in allLocalVars:
            #    allLocalVars.append(localVar)
            usedParameters = []
            usedParameterCounter = 0
            regNum = usedParameterCounter
            plusCounter = 0
            plusLocation = []
            constantLocation = []
            for element in array:
                if element == "+":
                    plusCounter += 1
                    plusLocation.append(array.index(element))
            for parameter in parameters:
                if parameter in array:
                    usedParameters.append(parameter)

            if len(usedParameters) < plusCounter + 1:
                for location in plusLocation:
                    if array[location - 1] not in usedParameters:
                        if array[location - 1] not in allLocalVars and not array[location + 1].isdigit():
                            return "Error: variable " + array[location - 1] + " is undeclared."
                        else:
                            constantLocation.append(location - 1)
                    if array[location + 1] not in usedParameters:
                        constantLocation.append(location + 1)
                        if array[location + 1] not in allLocalVars and not array[location + 1].isdigit():
                            return "Error: variable " + array[location + 1] + " is undeclared."
                        else:
                            constantLocation.append(location + 1)

            # generating instructions
            for element in array:
                if element in allLocalVars or usedParameters:
                    instr = "LDR R" + str(regNum) + ", FP, " + str(symbolT[element]) + "; read " + element + "\n"
                    output.append(instr)
                    regNum += 1

            for location in constantLocation:
                instr = "AND R" + str(regNum) + ", R" + str(regNum) + ", 0; clear R" + str(regNum) + "\n"
                output.append(instr)
                instr = "ADD R" + str(regNum) + ", R" + str(regNum) + ", " + str(array[location]) + "; add " + str(
                    array[location]) + " to R" + str(regNum) + "\n"
                output.append(instr)
                regNum += 1

            i = 0
            for i in range(plusCounter):
                instr = "ADD R0, R" + str(i) + ", R" + str(i + 1) + "; put sum in R0" + "\n"
                output.append(instr)
                i += 1
            instr = "STR R0, FP, 3; write RV" + "\n"
            output.append(instr)
    file1 = open(file+'_output.lc3', 'w')
    file1.writelines(output)  ###output
    file1.close()  # Closing file
    return "File " + file + " compiled successfully without error."

if __name__ == '__main__':
    # print(CreateSymbolTable("sample.code"))
    # print(SyntaxCheck("illegal.code"))
    # print(AssemblyGenerator("sample.code"))
    print(AssemblyGeneratorKevin("sample.code"))
    print(AssemblyGeneratorKevin("multi.code"))
    print(AssemblyGeneratorKevin("declare2.code"))
    print(AssemblyGeneratorKevin("undeclared1.code"))
    print(AssemblyGeneratorKevin("undeclared2.code"))
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
    '''

    # 40184/index.html
    # 43210/choose-db?db=mongo
#             :30046
# 165.106.10.170:50515/index.html
# 40404/pickDatabase?dbchoice=mongo
