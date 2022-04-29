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
            new_array = line.split(",")
            for declaration in new_array:
                #print(declaration)
                #print(declaration[0:3])
                if declaration[0:3] != "int":
                    declaration = "int " + declaration
                code.insert(code.index(line), declaration)
            #for newline in code:
            #    print(newline)
            line = new_array[0]
            #newline = "int"+line[line.index(",")+1:]
            #code.insert(code.index(line),newline)
            #line = line[:line.index(",")]
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
            print(constantLocation)
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
