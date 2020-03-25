"""CPU functionality."""

import sys

LDI = 0b10000010
PRN = 0b01000111
PRA = 0b01001000
HLT = 0b00000001
ST = 0b10000100
LD = 0b10000011
ADD = 0b10100000
SUB = 0b10100001
MUL = 0b10100010
DIV = 0b10100011
MOD = 0b10100100
DEC = 0b01100110
INC = 0b01100101
CMP = 0b10100111
AND = 0b10101000
OR = 0b10101010
XOR = 0b10101011
NOT = 0b01101001
SHL = 0b10101100
SHR = 0b10101101
PUSH = 0b01000101
POP = 0b01000110
CALL = 0b01010000
RET = 0b00010001
EMP = 0b00000000

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = self.reg[0]
        self.sp = 7
        self.instruction = {
            LDI: lambda register, value: self.handle_LDI(register, value),
            PRN: lambda value, _: print(self.reg[value]),
            ADD: lambda reg_a, reg_b: self.alu('ADD', reg_a, reg_b),
            MUL: lambda reg_a, reg_b: self.alu('MUL', reg_a, reg_b),
            CMP: lambda reg_a, reg_b: self.alu('CMP', reg_a, reg_b)
        }

    def handle_LDI(self, register, value):
            self.reg[register] = value

    def ram_read(self, MAR): #memory address register
        return self.ram[MAR]

    def ram_write(self, MAR, MDR): #memory data register
        self.ram[MAR] = MDR

    def load(self, program):
        """Load a program into memory."""
        address = 0
        # program = [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111, # PRN R0
        #     0b00000000,
        #     0b00000001, # HLT
        # ]

        with open(program) as file:
            for line in file:
                command = line.strip().split('#')
                num_return = command[0].strip()

                if num_return != "":
                    num = int(num_return, 2)
                    self.ram[address] = num
                    address += 1
                else:
                    continue
        #     try:
        #         self.ram_write(int(command, 2), address)
        #         address += 1
        #     except ValueError:
        #         pass

        #     for instruction in program:
        #         self.ram[address] = instruction
        #         address += 1
        # file.close()
    
    # def HLT(self, op1, op2):
    #     return (0, False)
    
    # def LDI(self, op1, op2):
    #     self.reg[op1] = op2
    #     return (3, True)

    # def PRN(self, op1, op2):
    #     print(self.reg[op1])
    #     return (2, True)
    
    # def MUL(self, op1, op2):
    #     self.alu('MUL', op1, op2)
    #     return (3, True)

    def alu(self, op, reg_a, reg_b = None):
        """ALU operations."""

        def add(reg_a, reg_b):
            self.reg[reg_a] += self.reg[reg_b]
        def mul(reg_a, reg_b):
            self.reg[reg_a] *= self.reg[reg_b]
        
        alu_math = {
            'ADD': add,
            'MUL': mul
        }

        if op in alu_math:
            alu_math[op](reg_a, reg_b)
        # if op == "ADD":
        #     self.reg[reg_a] += self.reg[reg_b]
        # elif op == "MUL":
        #     self.reg[reg_a] *= self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        while True:
            IT = self.ram[self.pc]
            op1 = self.ram_read(self.pc + 1)
            op2 = self.ram_read(self.pc + 2)

            if IT == HLT:
                return False
            
            if IT == EMP:
                continue

            if IT in self.instruction:
                self.instruction[IT](op1, op2)
                operand = IT >> 6
                setp = (IT & 0b10000) >> 4

                if not setp:
                    self.pc += operand + 1

