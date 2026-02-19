def register_file_generator() -> list[int]:
    return [         # reg. index
        0x00000000,  # 0
        0x00000000,  # 1
        0x7fffeffc,  # 2
        0x10008000,  # 3
        0x00000000,  # 4
        0x10010000,  # 5
        0x00400000,  # 6
        0x000d2a56,  # 7
        0x00000006,  # 8
        0x00000001,  # 9
        0x00000000, # 10
        0x00000000, # 11
        0x00000000, # 12
        0x00000000, # 13
        0x00000000, # 14
        0x00000000, # 15
        0x00000000, # 16
        0x00000000, # 17
        0x1001000c, # 18
        0x00000000, # 19
        0xff000000, # 20
        0x00000000, # 21
        0x00000014, # 22
        0x00000000, # 23
        0x00000000, # 24
        0x00000000, # 25
        0x00000000, # 26
        0x00000000, # 27
        0x7ab0014e, # 28
        0x1200ffff, # 29
        0x112ec218, # 30
        0x00a000b0  # 31
    ]


def memory_text_allocation(memory: dict[int, int]) -> dict[int, int]:
    """
    Populates the text memory, respresented as a dict, with the address and the instruction
    """
    with open("machine_code.txt", "r") as machine_code:
        current_address = 0x00400000
        for instruction in machine_code:
            memory[current_address] = int(instruction.strip("\n"), 2) 
            current_address += 4
    return memory


def memory_data_allocation(memory: dict[int, int]) -> dict[int, int]:
    """
    Populates the data memory, respresented as a dict, with the address and the value
    """
    ret_memory = memory
    current_address = 0x10010000
    for _ in range(32): # 128-byte memory
        ret_memory[current_address] = 0
        current_address += 4
    return ret_memory


# Initialises CPU registers and memory
def init():
    register_file = register_file_generator()
    memory = {}
    memory = memory_text_allocation(memory)
    memory = memory_data_allocation(memory)

    return register_file, memory