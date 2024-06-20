Instruction_Memory_fac = {
	4194304: 0x3c011001,  # lui $a1,4097
	4194308: 0x8c280000,  # lw $t0,0($a1)
	4194312: 0x20090001,  # addi $t1,$0,1
	4194316: 0x11000004,  # beq $t0,$0,4
	4194320: 0x71284802,  # mul $t1,$t1,$t0
	4194324: 0x20010001,  # addi $a1,$0,1
	4194328: 0x01014022,  # sub $t0,$t0,$a1
	4194332: 0x08100003,  # j 4194316
	4194336: 0x3c011001,  # lui $a1,4097
	4194340: 0xac290004  # sw $t1,4($a1)
}

Instruction_Memory_fib = {
    4194304 : 0x3c011001, # lui $a1,4097
    4194308 : 0x8c280000, # lw $t0,0($a1)
    4194312 : 0x20090000, # addi $t1,$0,0
    4194316 : 0x200a0001, # addi $t2,$0,1
    4194320 : 0x20010001, # addi $a1,$0,1
    4194324 : 0x01014022, # sub $t0,$t0,$a1
    4194328 : 0x11000004, # beq $t0,$0,4
    4194332 : 0x01495820, # add $t3,$t2,$t1
    4194336 : 0x000a4820, # add $t1,$0,$t2
    4194340 : 0x000b5020, # add $t2,$0,$t3
    4194344 : 0x08100004, # j 4194320
    4194348 : 0x3c011001, # lui $a1,4097
    4194352 : 0xac2a0004  # sw $t2,4($a1)
}

Instruction_Memory_even_or_odd = {
    4194304 : 0x3c011001, # lui $1,4097
    4194308 : 0x8c280000, # lw $8,0($1)
    4194312 : 0x20090001, # addi $9,$0,1
    4194316 : 0x01285024, # and $10,$9,$8
    4194320 : 0x3c011001, # lui $1,4097
    4194324 : 0xac2a0004 # sw $10,4($1)
}

Data_Memory_fac = {268500992: 5, 268500996: 0}
Data_Memory_fib = {268500992: 8, 268500996: 0}
Data_Memory_even_or_odd = {268500992: 2654, 268500996: 0}

class Processor:
    def __init__(self, Instruction_Memory, Data_Memory):
        self.reg = [0] * 32
        self.instr_mem = Instruction_Memory
        self.data_mem = Data_Memory
        self.pc = 4194304

    # FETCH STAGE
    def fetch(self):
        instruction = self.instr_mem[self.pc] #fetching instruction
        self.pc += 4 #incrementing pc
        return instruction

    # DECODE STAGE
    def decode(self, instruction):
        op = (instruction >> 26) & 0x3F  # 6bit
        rs = (instruction >> 21) & 0x1F  # 5bit
        rt = (instruction >> 16) & 0x1F  # 5bit
        rd = (instruction >> 11) & 0x1F  # 5bit
        shamt = (instruction >> 6) & 0x1F  # 5bit
        funct = (instruction) & 0x3F  # 6bit
        imm = (instruction) & 0xFFFF  # 16bit
        address = (instruction) & 0x3FFFFFF  # 26bit
        return op, rs, rt, rd, shamt, funct, imm, address

    # EXECUTE STAGE
    def execute(self, op, rs, rt, rd, shamt, funct, imm, address):
        if op == 35:  # lw 
            address = self.reg[rs] + imm 
            data = self.data_mem[address]
            return data 

        elif op == 43:  # sw
            address = self.reg[rs] + imm
            data = self.reg[rt]
            self.data_mem[address] = data

        elif op == 15:  # lui
            address = (imm << 16)
            return address

        elif op == 0:  # R-type
            if funct == 32:  # add
                return self.reg[rs] + self.reg[rt]
            elif funct == 34:  # sub
                return self.reg[rs] - self.reg[rt]
            elif funct == 36:  # and
                return self.reg[rs] & self.reg[rt]
            elif funct == 37:  # or
                return self.reg[rs] | self.reg[rt]
            elif funct == 42:  # slt
                if self.reg[rs] < self.reg[rt]:
                    return 1
                else:
                    return 0
            elif funct == 0:  # sll
                return self.reg[rt] << shamt
            elif funct == 2:  # srl
                return self.reg[rt] >> shamt

        elif op == 28 and funct == 2:  # mul
            return self.reg[rs] * self.reg[rt]

        elif op == 8:  # addi
            return self.reg[rs] + imm
        elif op == 12:  # andi
            return self.reg[rs] & imm
        elif op == 13:  # ori
            return self.reg[rs] | imm

        elif op == 4:  # beq
            if self.reg[rs] == self.reg[rt]:
                self.pc += (imm * 4)

        elif op == 5:  # bne
            if self.reg[rs] != self.reg[rt]:
                self.pc += (imm * 4)

        elif op == 2:  # j
            self.pc = (self.pc & 0xF0000000) | (address << 2) #adding 4 sign digits at the beginning and 2 0s at the end to make 26 bit addresss to 32 bit
        return

    # MEMORY ACCESS STAGE
    def memory_access(self, result):
        return result

    # WRITE BACK STAGE
    def write_back(self, op, data, rd, rt):
        if (op == 0 or op == 28):  # for R-type instructions
            self.reg[rd] = data
        else: # for I-type instructions
            self.reg[rt] = data

    def run(self):
        while self.pc < 4194304 + (4 * len(self.instr_mem)): #condition for 
            instruction = self.fetch()
            op, rs, rt, rd, shamt, funct, imm, address = self.decode(instruction)
            result = self.execute(op, rs, rt, rd, shamt, funct, imm, address)
            if result is not None:
                data = self.memory_access(result)
                self.write_back(op, data, rd, rt)

    def reg_name(self, reg_num):
        if reg_num == 0:
            return "0"
        elif reg_num == 31:
            return "ra"
        elif reg_num == 1:
            return "at"
        elif 2 <= reg_num <= 3:
            return f"v{reg_num - 2}"
        elif 4 <= reg_num <= 7:
            return f"a{reg_num - 4}"
        elif 8 <= reg_num <= 15:
            return f"t{reg_num - 8}"
        elif 16 <= reg_num <= 23:
            return f"s{reg_num - 16}"
        elif 24 <= reg_num <= 25:
            return f"t{reg_num - 24 + 2}"
        elif 26 <= reg_num <= 27:
            return f"k{reg_num - 26}"
        elif 28 <= reg_num <= 31:
            return f"g{reg_num - 28}"

    def print_reg(self):
        print("Registers:")
        for i, value in enumerate(self.reg):
            reg_name = self.reg_name(i)
            print(f"${reg_name}: {value}")
        print()

print('''Choose any of the following programs:
1. Factorial of n
2. Nth number in Fibonacci series
3. Finding if n is even or odd''')
print()

choice = int(input("Choice: "))
print()
if choice==1:
    pro1 = Processor(Instruction_Memory_fac, Data_Memory_fac)
    pro1.run()
    pro1.print_reg()
    print("The factorial of n is:")
    print(pro1.data_mem[268500996])
elif choice==2:
    pro2 = Processor(Instruction_Memory_fib, Data_Memory_fib)
    pro2.run()
    pro2.print_reg()
    print("The nth number in Fibonacci series is:")
    print(pro2.data_mem[268500996])
elif choice==3:
    pro3 = Processor(Instruction_Memory_even_or_odd, Data_Memory_even_or_odd)
    pro3.run()
    pro3.print_reg()
    print("Note: Getting a boolean result 1 means that the given integer is odd, while getting a 0 implies that given integer is even")
    print("Boolean result :")
    print(pro3.data_mem[268500996])
else:
    print("Invalid input")