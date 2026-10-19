# Single cycle RISC-V CPU
Basic implementation of a single cycle RISC-V CPU in Python.

## How it started
After the end of the first year's first semester at FEUP, studying Computer Science (L.EIC - Licenciatura em Engenharia Informática e Computação), me and other two friends decided to code a simple implementation of a single-cycle CPU, that supports some of the instructions of the RISC-V ISA (Instruction Set Architecture), since it was, for us, the most interesting topic of one of our courses, FSC (Fundamentos de Sistemas Computacionais).

## Supported instructions

The implemented CPU is able to interpret and execute the following RISC-V instructions:

* R-type: `add`, `sub`, `and`, `or`
* I-type: `lw`
* S-type: `sw`

## Implementation details

The instructions are read from a text file named `riscv_code.txt`, where each line contains a single instruction in RISC-V assembly language.

The CPU is able to access its 32 registers and a (fictitious) memory of 128 bytes.

## How to use

1. Clone the repository.
2. Write the desired RISC-V instructions to be executed in the file `riscv_code.txt`.
   
     * Here are examples of set of instructions to try (copy these into the `riscv_code.txt`):
        * Example 1:

        ```txt
        add x5, x5, x5
        add x6, x5, x0
        ```

        * Example 2:

        ```txt
        lw x5, 0(x6)
        sw x5, 8(x6)
        add x5, x5, x5
        sub x6, x30, x31
        ```

        * Example 3:

        ```txt
        and x5, x0, x30
        or x6, x30, x31
        or x7, x5, x6
        sub x30, x7, x6
        ```

        * Example 4:

        ```txt
        sw x30, 12(x5)
        lw x6, 0(x18)
        or x6, x6, x0
        ```

        * Example 5:

        ```txt
        sw x29, 20(x5)
        add x27, x5, x22
        lw x7, 0(x27)
        sub x7, x0, x7
        sub x7, x0, x7
        or x7, x7, x7
        add x6, x7, x0
        and x5, x20, x6
        ```

  
3. In the project's root directory, run the command:

```shell
python3 cpu.py
```

4. See the results of the instruction execution in the printed register values. The registers and memory addresses whose values were modified during the execution of the program are highlighted in the output in the `Final Register File` and `Final Memory` section.

## Developers

This project was developed by:

* Gabriel Magalhães (<up202405890@up.pt>)
* Guilherme Cunha (<up202405961@up.pt>)
* Pedro Pires (<up202405967@up.pt>)
