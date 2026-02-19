def register_file_pre(register_file: list[int]):
    """
    Displays register file before execution
    """
    # Header
    print("-" * 26)
    print("Register Name   Values")
    print(register_file)
    for reg_i, value in enumerate(register_file):
        # Creates the name of the register, ex: x8
        register_name = "x" + str(reg_i)

        # Format string -> align the register name to the left and display registers as hexadecimal 

        print(f"{register_name:<4}\t\t{value:#010x}")
    
    print()


def memory_pre(memory: dict[int, str]):
    """
    Displays memory before execution
    """

    # Header
    print("-" * 26)
    print("Memory address   Values")

    for address, value in memory.items():
        print(f"{address:#010x}\t {value:#010x}")

    print()


def register_file_post(start_register_file: list[int], register_file: list[int]):
    """
    Displays register after before execution
    """
    # Header
    print("-" * 26)
    print("Register Name   Values")

    for reg_i, value in enumerate(register_file):
        # Creates the name of the register, ex: x8
        register_name = "x" + str(reg_i)
        # Format string -> align the register name to the left and display registers as hexadecimal 

        if value == start_register_file[reg_i]:
            print(f"{register_name:<4}\t\t{value:#010x}")
        else:
            print(f"{'\033[33m'}{register_name:<4}{'\033[0m'}\t\t{'\033[33m'}{value:#010x}{'\033[0m'}")  
    print()


def memory_post(start_memory: dict[int, int], memory: dict[int, int]):
    """
    Displays memory after execution
    """

    # Header
    print("-" * 26)
    print("Memory address   Values")

    for address, value in memory.items():

        if value == start_memory[address]:
            print(f"{address:#010x}\t {value:#010x}")
        else:
            print(f"{'\033[33m'}{address:#010x}{'\033[0m'}\t {'\033[33m'}{value:#010x}{'\033[0m'}")
    print()