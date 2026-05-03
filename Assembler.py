import sys

if len(sys.argv) != 2:
    print("Usage: python assembler.py <filename.asm>")
    sys.exit(1)

filepath = sys.argv[1]
filepath1 = filepath.replace(".asm",".hack")

class counter():
    count = 16
    label = 0
    target_code = []
    var_table = {}
    tracker = {}

    def increment(self):
        counter.count += 1
    def add(self):
        counter.label += 1
    
target_code = []
var_table = {}
tracker = {}

def parse(filepath):                      #parsing
    instruction = []
    with open(filepath,'r') as f:
        for line in f:
            if "//" in line:
                line = line[:line.index("//")]
            line = line.strip()
            line = line.replace(" ","")
            if line == "":
                continue
            instruction.append(line)
    return instruction

def create_sym_table(instruction):      #  {START: (line index , rank of label)}  (both starts from 0)
    counter.tracker = {}
    x = counter()
    for i in instruction:
        if i[0] == '(':
            counter.tracker[i[1:-1]] = (instruction.index(i), x.label)
            x.add()

Instruction = parse(filepath)
create_sym_table(Instruction)



def A_inst(instruction):            # A instruction conversion
    nums = ['0','1','2','3','4','5','6','7','8','9']
    predefined = {
    "R0":0,"R1":1,"R2":2,"R3":3,"R4":4,"R5":5,"R6":6,"R7":7,
    "R8":8,"R9":9,"R10":10,"R11":11,"R12":12,"R13":13,"R14":14,"R15":15,
    "SCREEN":16384,"KBD":24576,
    "SP":0,"LCL":1,"ARG":2,"THIS":3,"THAT":4
    }
    if instruction[1] in nums:
        val = int(instruction[1:])
        val = format(val,"016b")
        return str(val)
    elif instruction[1:] in counter.tracker:
        val = counter.tracker[instruction[1:]][0] - counter.tracker[instruction[1:]][1]
        val = format(val,"016b")
        return str(val)
    elif instruction[1:] in predefined:
        val = predefined[instruction[1:]]
        val = format(val,"016b")
        return str(val)
    else:
        a = counter()
        if instruction[1:] in counter.var_table:
            val = counter.var_table[instruction[1:]]
            val = format(val,"016b")
            return str(val)
        else:
            counter.var_table[instruction[1:]] = counter.count     # {variable : RAM location}
            a.increment()
            val = counter.var_table[instruction[1:]]
            val = format(val,"016b")
            return str(val)

def C_comp(comp):
    ins = ""
    if len(comp) == 1:
        if comp == '0':
            ins = "101010"
        elif comp == '1':
            ins = '111111'
        elif comp == 'D':
            ins = '001100'
        else: 
            ins = "110000"
    elif len(comp) == 2:
        if comp[0] == '-':
            if comp[1] == '1':
                ins = '111010'
            elif comp[1] == 'D':
                ins = '001111'
            else:
                ins = '110011'
        else:
            if comp[1] == 'D':
                ins = '001101'
            else:
                ins = '110001'
    else:
        if comp[1] == '+':
            if comp[0] == 'D':
                if comp[2] == '1':
                    ins = '011111'
                else: 
                    ins = '000010'
            else:
                ins = '110111'
        elif comp[1] == '-':
            if comp[0] == 'D':
                if comp[2] == '1':
                    ins = '001110'
                else:
                    ins = '010011'
            else:
                if comp[2] == '1':
                    ins = '110010'
                else:
                    ins = '000111'
        elif comp[1] == '&':
            ins = '000000'
        else:
            ins = '010101'
    return ins 

def C_des(des):
    ins = ['0','0','0']
    if 'A' in des:
        ins[0] = '1'
    if 'D' in des:
        ins[1] = '1'
    if 'M' in des:
        ins[2] = '1'
    return "".join(ins)

def C_jmp(jmp):
    ins = '000'
    if jmp == "JGT":
        ins = '001'
    elif jmp == "JEQ":
        ins = '010'
    elif jmp == "JGE":
        ins = '011'
    elif jmp == "JLT":
        ins = '100'
    elif jmp == "JNE":
        ins = '101'
    elif jmp == "JLE":
        ins = '110'
    elif jmp =='JMP':
        ins = '111'
    return ins

def C_inst(instruction):
    a = 0
    if '=' in instruction and ';' in instruction:   # dest = comp;jmp
        dest1 = instruction[:instruction.index('=')]
        comp1 = instruction[instruction.index('=')+1:instruction.index(";")]
        jmp1 = instruction[instruction.index(";")+1:]
        dest = C_des(dest1)
        comp = C_comp(comp1)
        jmp  = C_jmp(jmp1)
    elif '=' in instruction:
        dest1 = instruction[:instruction.index('=')]
        comp1 = instruction[instruction.index('=')+1:]
        dest = C_des(dest1)
        comp = C_comp(comp1)
        jmp = '000'
    elif ';' in instruction:
        comp1 = instruction[:instruction.index(";")]
        jmp1 = instruction[instruction.index(";")+1:]
        comp = C_comp(comp1)
        jmp  = C_jmp(jmp1)
        dest = '000'

    if 'M' not in comp1:
        a=0
    else: 
        a=1
    
    return ( "111" + str(a) + comp + dest + jmp )

def translate(instruction):         #classifying instruction types
    if instruction[0] == '@':
        return 'A'
    elif instruction[0] == '(':
        return 'L'
    else:
        return 'C'

for ins in Instruction:             #operating based on type of instruction
    if translate(ins) == 'A':
        counter.target_code.append(A_inst(ins))
    elif translate(ins) == 'C':
        counter.target_code.append(C_inst(ins))
    else:
        continue

with open(filepath1, 'w') as f:
    for x in counter.target_code:
        f.write(x + "\n")


