import assembler
import display
import mem_regs

def control_unit(opcode:str) -> tuple[str, ...]:
    """
    Creates the control signs for a given operation
    """
    if opcode == "0000011": # I-type, lw
        Branch = "0"
        MemRead = "1"
        MemtoReg = "1"
        ALUOp = "00"
        MemWrite = "0"
        ALUSrc = "1"
        RegWrite = "1"

    elif opcode == "0100011":  # S-type, sw
        Branch = "0"
        MemRead = "0"
        MemtoReg = "0"
        ALUOp = "00"
        MemWrite = "1"
        ALUSrc = "1"
        RegWrite = "0"
        
    elif opcode == "1100011": # B-type
        Branch = "1"
        MemRead = "0"
        MemtoReg = "0"
        ALUOp = "01"
        MemWrite = "0"
        ALUSrc = "0"
        RegWrite = "0"
        
    else: # R-Type
        Branch = "0"
        MemRead = "0"
        MemtoReg = "0"
        ALUOp = "10"
        MemWrite = "0"
        ALUSrc = "0"
        RegWrite = "1"

    return Branch, MemRead, MemtoReg, ALUOp, MemWrite, ALUSrc, RegWrite


def pc_adder(pc:int) -> int:
    """
    Adds 4 to de PC (program counter)
    """
    return pc + 4



def instruction_memory(pc:int, memory:dict[int, int]) -> int:
    """
    Gets the instruction which corresponds to the current PC address
    """
    instruction = memory[pc]
    instruction = f"{instruction:032b}"
    return instruction


def imm_gen(instruction:str, opcode:str) -> str:
    """
    Generates the 32-bit immediate based on the instruction    
    """
    if opcode == "0000011": # I-type
        imm = instruction[:12]
        if imm[0] == "1":  #negative
            imm = "1" * (32-len(imm)) + imm
        else: #positive
            imm = "0" * (32-len(imm)) + imm
            
    elif opcode == "0100011": # S-type
        imm = instruction[:7] + instruction[20:25]
        if imm[0] == "1":  #negative
            imm = "1" * (32-len(imm)) + imm
        else: #positive
            imm = "0" * (32-len(imm)) + imm
            
    elif opcode == "1100011":
        # B-type
        imm = instruction[0] + instruction[24] + instruction[1:7] + instruction[20:24] + "0"
        if imm[0] == "1":  #negative
            imm = "1" * (32-len(imm)) + imm
        else: #positive
            imm = "0" * (32-len(imm)) + imm
    else:
        return "0"
    
    return imm


def twos_complement_reader(num:str) -> int:
    first_bit = int(num[0])
    exp = len(num)-1
    res = -2 ** exp * first_bit
    for bit in num[1:]:
        exp -= 1
        res += 2**exp * int(bit)
    return res    


def branch_adder(pc:int, imm:int) -> int:
    """
    Adds the immediate in the branch instruction and adds it do PC
    """
    return pc + imm + 4


def ALU_control(funct7:str, funct3:str, ALUOp:str) -> str:
    if ALUOp == "00":
        return "add"
    
    elif ALUOp == "01":
        return "subtract"
    
    elif ALUOp == "10":
        if funct7 == "0000000":
            if funct3 == "000":
                return "add"
            elif funct3 == "111":
                return "and"
            elif funct3 == "110":
                return "or"
        else:
                return "subtract"
        

def registers(rs1: int, rs2: int, rd: int, write_data: None, RegWrite: str, register_file: list[int]):
    read_data_1 = register_file[rs1]
    read_data_2 = register_file[rs2]
    if RegWrite == "1" and write_data != None:
        register_file[rd] = write_data
        return register_file
    return read_data_1, read_data_2


def ALUSrc_MUX(ALUSrc:str, read_data_2:int, imm:int) -> int:
    if ALUSrc == "1":
        return imm
    return read_data_2


def ALU(op:str, read_data_1:int, second_op:int) -> tuple[int, str]:

    if op == "add":
        res = read_data_1 + second_op
        ALU_result = res
    
    elif op == "subtract":
        res = read_data_1 - second_op
        ALU_result = res

    else:
        res = ""
        read_data_1_bin = assembler.binary_converter(read_data_1, 32)
        read_data_2_bin = assembler.binary_converter(second_op, 32)
        if op == "and":
            for index, bit in enumerate(read_data_1_bin):
                res += AND(bit, read_data_2_bin[index])
        else: # or
            for index, bit in enumerate(read_data_1_bin):
                res += OR(bit, read_data_2_bin[index])
        ALU_result = twos_complement_reader(res)
    
    Zero = "0"
    if read_data_1 == second_op:
        Zero = "1"
        
    return ALU_result, Zero


def AND(x:str, y:str) -> str:
    if x == "1" and y == "1":
        return "1"
    return "0"


def OR(x:str, y:str) -> str:
    if x == "1" or y == "1":
        return "1"
    return "0"


def data_memory(address:int, write_data:int, MemWrite:str, MemRead:str, memory: dict[int, int]) -> None | int:
    if MemRead == "1":
        read_data = memory[address]
    else:
        read_data = None

    if MemWrite == "1":
        memory[address] = write_data
        
    return read_data


def MemtoReg_MUX(read_data: None | int, ALU_result:int, MemtoReg:str) -> None | int:
    if MemtoReg == "0":
        return ALU_result
    elif read_data != None:
        return read_data
    return None


def PCSrc_MUX(res_pc_adder:int, res_branch_adder:int, Branch:str, Zero:str) -> int:
    
    if AND(Branch, Zero) == "1":
        PCScr = "1"
    else:
        PCScr = "0"

    if PCScr == "0":
        return res_pc_adder
    else:
        return res_branch_adder


def main():
    pc = assembler.main()
    register_file, memory = mem_regs.init()

    # To show the differences before and after the execution of the RISC-V instructions
    start_register_file = register_file.copy() 
    start_memory = memory.copy()

    print("Initial Register File")
    display.register_file_pre(register_file)

    print("Initial Memory")
    display.memory_pre(memory)

    while pc in memory.keys():
        #pc adder
        res_pc_adder = pc_adder(pc)

        # Gets the instruction
        instruction = instruction_memory(pc, memory)

        #Slices the instruction
        opcode = instruction[25:]
        funct7 = instruction[:7]
        funct3 = instruction[17:20]
        rs1 = int(instruction[12:17], 2)
        rs2 = int(instruction[7:12], 2)
        rd = int(instruction[20:25], 2)

        # Signals from the control unit
        Branch, MemRead, MemtoReg, ALUOp, MemWrite, ALUSrc, RegWrite = control_unit(opcode)

        # ImmGen unit
        imm = imm_gen(instruction, opcode)

        # Branch_adder
        imm = twos_complement_reader(imm)
        res_branch_adder = branch_adder(pc, imm)

        # ALU_Control
        ALU_operation = ALU_control(funct7, funct3, ALUOp)

        # Registers
        read_data_1, read_data_2 = registers(rs1, rs2, rd, None, RegWrite, register_file)

        #ALUScr_MUX
        second_op = ALUSrc_MUX(ALUSrc, read_data_2, imm)

        #ALU
        ALU_result, Zero = ALU(ALU_operation, read_data_1, second_op)

        #Data_Memory
        read_data = data_memory(ALU_result, read_data_2, MemWrite, MemRead, memory)

        #MemToReg_MUX
        write_data = MemtoReg_MUX(read_data, ALU_result, MemtoReg)

        #registers
        if RegWrite == "1":
            register_file = registers(rs1, rs2, rd, write_data, RegWrite, register_file)

        # PCSrc_MUX
        pc = PCSrc_MUX(res_pc_adder, res_branch_adder, Branch, Zero)
    
    print("Final Register File")
    display.register_file_post(start_register_file, register_file)

    print("Final Memory")
    display.memory_post(start_memory, memory)
    

if __name__ == "__main__":
    main()
