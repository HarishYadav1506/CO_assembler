def splits(z):
    lst = []
    lst.append(z[0:2])
    lst.append(z[3:5])
    lst.append(z[6:8])
    return lst

def decimal_to_binary(decimal_num, num_bits):
    if decimal_num < 0:
        binary_num = bin(decimal_num & int("1"*num_bits, 2))[2:]
        binary_num = '1' + binary_num.zfill(num_bits - 1)  
    else:
        binary_num = bin(decimal_num)[2:].zfill(num_bits)  
    return binary_num

registers = {
    "zero": "00000", "ra": "00001", "sp": "00010", "gp": "00011", "tp": "00100", "t0": "00101", "t1": "00110",
    "t2": "00111", "s0": "01000", "fp": "01000", "s1": "01001", "a0": "01010", "a1": "01011", "a2": "01100",
    "a3": "01101", "a4": "01110", "a5": "01111", "a6": "10000", "a7": "10001", "s2": "10010", "s3": "10011",
    "s4": "10100", "s5": "10101", "s6": "10110", "s7": "10111", "s8": "11000", "s9": "11001", "s10": "11010",
    "s11": "11011", "t3": "11100", "t4": "11101", "t5": "11110", "t6": "11111"
}

R_type = ["add", "sub", "sll", "slt", "sltu", "xor", "srl", "or", "and"]
I_type = ["lw", "addi", "sltiu", "jalr"]
S_type = ["sw"]
B_type = ["beq", "bne", "blt", "bge", "bltu", "bgeu"]
U_type = ["lui", "auipc"]
J_type = ["jal"]

opcode = {
    "add": "0110011", "sub": "0110011", "sll": "0110011", "slt": "0110011", "sltu": "0110011", "xor": "0110011",
    "srl": "0110011", "or": "0110011", "and": "0110011", "lw": "0000011", "addi": "0010011", "sltiu": "0010011",
    "jalr": "1100111", "sw": "0100011", "beq": "1100011", "bne": "1100011", "blt": "1100011", "bge": "1100011",
    "bltu": "1100011", "bgeu": "1100011", "lui": "0110111", "auipc": "0010111", "jal": "1101111"
}

funct3 = {
    "add": "000", "sub": "000", "sll": "001", "slt": "010", "sltu": "011", "xor": "100", "srl": "101", "or": "110",
    "and": "111", "lw": "010", "addi": "000", "sltiu": "011", "jalr": "000", "sw": "010", "beq": "000", "bne": "001",
    "blt": "100", "bge": "101", "bltu": "110", "bgeu": "111"
}

funct7 = {
    "add": "0000000", "sub": "0100000", "sll": "0000000", "slt": "0000000", "sltu": "0000000", "xor": "0000000",
    "srl": "0000000", "or": "0000000", "and": "0000000"
}

output = []

with open('arg.txt', 'r') as file:
    lines = file.readlines()
    for i in lines:
        i = i.strip() 
        if not i:  
            continue
            
        if i == "beq zero,zero,0":
            output.append("00000000000000000000000001100011") 
            continue
            
        b = i.split()
        if not b:  
            continue

        instruction = b[0].lower() 

        if instruction in R_type:
            c = b[1].split(',')
            if len(c) != 3:
                output.append("Invalid instruction format")
                continue
            if all(reg.lower() in registers for reg in c):
                a = funct7[instruction] + registers[c[2].lower()] + registers[c[1].lower()] + funct3[instruction] + registers[c[0].lower()] + opcode[instruction]
                output.append(a)
            else:
                output.append("Register doesn't exist")

        elif instruction in I_type:
            if instruction == "lw":
                c = splits(b[1])
                if len(c) != 3:
                    output.append("Invalid instruction format")
                    continue
                if all(reg.lower() in registers for reg in [c[0], c[2]]):
                    try:
                        imm = int(c[1])
                        a = decimal_to_binary(imm, 12) + registers[c[2].lower()] + funct3[instruction] + registers[c[0].lower()] + opcode[instruction]
                        output.append(a)
                    except ValueError:
                        output.append("Invalid immediate value")
                else:
                    output.append("Register doesn't exist")
            else:
                c = b[1].split(',')
                if len(c) != 3:
                    output.append("Invalid instruction format")
                    continue
                if all(reg.lower() in registers for reg in c[:2]):
                    try:
                        imm = int(c[2])
                        a = decimal_to_binary(imm, 12) + registers[c[1].lower()] + funct3[instruction] + registers[c[0].lower()] + opcode[instruction]
                        output.append(a)
                    except ValueError:
                        output.append("Invalid immediate value")
                else:
                    output.append("Register doesn't exist")

        elif instruction in S_type:
            c = splits(b[1])
            if len(c) != 3:
                output.append("Invalid instruction format")
                continue
            if all(reg.lower() in registers for reg in [c[0], c[2]]):
                try:
                    imm = int(c[1])
                    z = decimal_to_binary(imm, 12)
                    a = z[0:7] + registers[c[0].lower()] + registers[c[2].lower()] + funct3[instruction] + z[7:12] + opcode[instruction]
                    output.append(a)
                except ValueError:
                    output.append("Invalid immediate value")
            else:
                output.append("Register doesn't exist")

        elif instruction in B_type:
            c = b[1].split(',')
            if len(c) != 3:
                output.append("Invalid instruction format")
                continue
            if all(reg.lower() in registers for reg in c[:2]):
                try:
                    imm = int(c[2])
                    z = decimal_to_binary(imm, 13)  # B-type uses 13-bit immediate
                    a = z[0] + z[2:8] + registers[c[1].lower()] + registers[c[0].lower()] + funct3[instruction] + z[8:12] + z[1] + opcode[instruction]
                    output.append(a)
                except ValueError:
                    output.append("Invalid immediate value")
            else:
                output.append("Register doesn't exist")

        elif instruction in U_type:
            c = b[1].split(',')
            if len(c) != 2:
                output.append("Invalid instruction format")
                continue
            if c[0].lower() in registers:
                try:
                    imm = int(c[1])
                    z = decimal_to_binary(imm, 32)
                    a = z[0:20] + registers[c[0].lower()] + opcode[instruction]
                    output.append(a)
                except ValueError:
                    output.append("Invalid immediate value")
            else:
                output.append("Register doesn't exist")

        elif instruction in J_type:
            c = b[1].split(',')
            if len(c) != 2:
                output.append("Invalid instruction format")
                continue
            if c[0].lower() in registers:
                try:
                    imm = int(c[1])
                    z = decimal_to_binary(imm, 21) 
                    a = z[0] + z[10:20] + z[9] + z[1:9] + registers[c[0].lower()] + opcode[instruction]
                    output.append(a)
                except ValueError:
                    output.append("Invalid immediate value")
            else:
                output.append("Register doesn't exist")

        else:
            output.append("Instruction doesn't exist")
with open('output.txt', 'w') as file:
    for line in output:
        file.write(line + '\n')
