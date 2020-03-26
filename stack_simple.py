# # Pushes 65, 99 on the stack
# # Pops 99, 65 off the stack (and prints it)
# 1      # PRINT_BEEJ
# 4      # SAVE 65 in reg 2
# 65
# 2
# 7      # PUSH reg 2
# 2
# 4      # SAVE 99 in reg 2
# 99
# 2
# 7      # PUSH reg 2
# 2
# 8      # POP reg 0
# 0
# 5      # PRINT_REGISTER reg 0
# 0
# 8      # POP reg 0
# 0
# 5      # PRINT_REGISTER reg 0
# 0
# 2      # HALT
# Collapse



#1:31

###cont simple code
import sys

PRINT_BEEJ     = 1
HALT           = 2
PRINT_NUM      = 3
SAVE           = 4  # Save a value to a register
PRINT_REGISTER = 5  # Print a value from a register
ADD            = 6  # regA += regB
PUSH           = 7
POP            = 8

memory = [None] * 256

register = [0] * 8

pc = 0
running = True

SP = 7

def load_memory(filename):
    address = 0
    try:
        with open(filename) as f:
            for line in f:

                # Ignore comments
                comment_split = line.split("#")

                # Strip out whitespace
                num = comment_split[0].strip()

                # Ignore blank lines
                if num == '':
                    continue

                val = int(num)
                memory[address] = val
                address += 1

    except FileNotFoundError:
        print("File not found")
        sys.exit(2)


if len(sys.argv) != 2:
    print("usage: simple.py filename")
    sys.exit(1)

filename = sys.argv[1]
load_memory(filename)

while running:
    command = memory[pc]

    if command == PRINT_BEEJ:
        print("Beej!")
        pc += 1

    elif command == HALT:
        running = False
        pc += 1

    elif command == PRINT_NUM:
        num = memory[pc + 1]
        print(num)
        pc += 2

    elif command == SAVE:
        num = memory[pc + 1]
        reg = memory[pc + 2]
        register[reg] = num
        pc += 3

    elif command == PRINT_REGISTER:
        reg = memory[pc + 1]
        print(register[reg])
        pc += 2

    elif command == ADD:
        reg_a = memory[pc + 1]
        reg_b = memory[pc + 2]
        register[reg_a] += register[reg_b]
        pc += 3

    elif command == PUSH:
        reg = memory[pc + 1]
        val = register[reg]
        # Decrement the SP.
        register[SP] -= 1
        # Copy the value in the given register to the address pointed to by SP.
        memory[register[SP]] = val
        pc += 2

    elif command == POP:
        reg = memory[pc + 1]
        val = memory[register[SP]]
        # Copy the value from the address pointed to by SP to the given register.
        register[reg] = val
        # Increment SP.
        register[SP] += 1
        pc += 2

    else:
        print(f"Unknown instruction: {command}")
        sys.exit(1)

