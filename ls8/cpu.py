"""CPU functionality."""
import sys, inspect, re

alu_operations = {
    'AND': 0b10101000,
    'OR': 0b10101010,
    'XOR': 0b10101011,
    'NOT': 0b01101001,
    'SHL': 0b10101100,
    'SHR': 0b10101101,
    'MOD': 0b10100100
}
class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        self.sp = 7
        self.reg[self.sp] = 0xF4
        self.halted = False
        self.instruction = {
            0b10100000: self.ADD,
            0b00000001: self.HLT,
            0b10000010: self.LDI,
            0b01000111: self.PRN,
            0b10100010: self.MUL,
            0b01000101: self.PUSH,
            0b01000110: self.POP,
            0b01010000: self.CALL,
            0b00010001: self.RET,
            0b10100111: self.CMP,
            0b01010100: self.JMP,
            0b01010101: self.JEQ,
            0b01010110: self. JNE
        }

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
                
    def ADD(self):
        self.alu('ADD', self.ram_read(self.pc+1),self.ram_read(self.pc+2))
        self.pc += 3

    def HLT(self):
        self.halted = True
        self.pc += 1
    
    def LDI(self):
        self.reg[self.ram_read(self.pc+1)] = self.ram_read(self.pc+2)
        self.pc += 3

    def PRN(self):
        print(self.reg[self.ram_read(self.pc+1)])
        self.pc += 2
    
    def MUL(self):
        reg_a = self.ram_read(self.pc+1)
        reg_b = self.ram_read(self.pc+2)
        self.alu('MUL', reg_a, reg_b)
        self.pc += 3
    
    def PUSH(self, MDR=None):
        self.reg[self.sp] -= 1
        data = MDR if MDR else self.reg[self.ram[self.pc+1]]
        self.ram_write(self.reg[self.sp], data)
        self.pc += 2

    def POP(self):
        self.reg[self.ram_read(self.pc+1)] = self.ram_read(self.reg[self.sp])
        self.pc += 2
        self.reg[self.sp] += 1

    def CALL(self):
        self.PUSH(self.pc+2)
        self.pc = self.reg[self.ram_read(self.pc-1)]

    def RET(self):
        self.pc = self.ram_read(self.reg[self.sp])
        self.reg[self.sp] += 1
    
    def CMP(self):
        reg_a = self.ram_read(self.pc+1)
        reg_b = self.ram_read(self.pc+2)
        value_1 = self.reg[reg_a]
        value_2 = self.reg[reg_b]
        if value_1 == value_2:
            self.e = 1
        else:
            self.e = 0
        self.pc += 3
    
    def JMP(self):
        reg_a = self.ram_read(self.pc+1)
        self.pc = self.reg[reg_a]

    def JEQ(self):
        reg_a = self.ram_read(self.pc+1)
        if self.e == 1:
            self.pc = self.reg[reg_a]
        else:
            self.pc += 2
    
    def JNE(self):
        reg_a = self.ram_read(self.pc+1)
        if self.e == 0:
            self.pc = self.reg[reg_a]
        else:
            self.pc += 2

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""
        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]

        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]

        elif op == alu_operations['AND']:
            self.reg[reg_a] &= self.reg[reg_b]
        
        elif op == alu_operations['OR']:
            self.reg[reg_a] |= self.reg[reg_b]

        elif op == alu_operations['XOR']:
            self.reg[reg_a] ^= self.reg[reg_b]

        elif op == alu_operations['NOT']:
            self.reg[reg_a] = ~self.reg[reg_a]

        elif op == alu_operations['SHL']:
            self.reg[reg_a] <<= self.reg[reg_b]

        elif op == alu_operations['SHR']:
            self.reg[reg_a] >>= self.reg[reg_b]

        elif op == alu_operations['MOD']:
            self.reg[reg_a] %= self.reg[reg_b]

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
        while not self.halted:
            IR = self.ram_read(self.pc)
            self.instruction[IR]()