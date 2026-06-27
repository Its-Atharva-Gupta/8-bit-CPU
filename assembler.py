OPCODES = {
    "ADD": "0000",
    "SUB": "0001",
    "AND": "0010",
    "OR": "0011",
    "XOR": "0100",
    "LOAD": "0101",
    "JUMP": "0110",
    "JZ": "0111",
    "STORE": "1000",
    "LOADR": "1001",
    "MOV": "1110",
    "HALT": "1111",
}

REGISTERS = {
    "R0": "00",
    "R1": "01",
    "R2": "10",
    "R3": "11",
}


def parse_register(token):
    token = token.upper()
    if token in REGISTERS:
        return REGISTERS[token]
    if token in REGISTERS.values():
        return token
    raise ValueError(f"Invalid register: {token}")


def assemble_line(line):
    line = line.split("#", 1)[0].strip().upper()
    if not line:
        return None

    parts = line.replace(",", " ").split()
    instr = parts[0]

    if instr in {"ADD", "SUB", "AND", "OR", "XOR", "MOV"}:
        if len(parts) != 3:
            raise ValueError(f"{instr} expects 2 register operands")
        opcode = OPCODES[instr]
        rd = parse_register(parts[1])
        rs = parse_register(parts[2])
        return opcode + rd + rs

    if instr == "LOAD":
        if len(parts) != 3:
            raise ValueError("LOAD expects a register and an immediate")
        opcode = OPCODES[instr]
        rd = parse_register(parts[1])
        imm = int(parts[2], 0)
        if imm < 0 or imm > 3:
            raise ValueError("Immediate must be 0-3")
        imm_bits = format(imm, "02b")
        return opcode + rd + imm_bits

    if instr in {"JUMP", "JZ"}:
        if len(parts) != 2:
            raise ValueError(f"{instr} expects a single address")
        opcode = OPCODES[instr]
        addr = int(parts[1], 0)
        if addr < 0 or addr > 15:
            raise ValueError("Address must be 0-15")
        addr_bits = format(addr, "04b")
        return opcode + addr_bits

    if instr == "STORE":
        if len(parts) != 3:
            raise ValueError("STORE expects a register and RAM address")
        opcode = OPCODES[instr]
        rs = parse_register(parts[1])
        addr = int(parts[2], 0)
        if addr < 0 or addr > 3:
            raise ValueError("RAM address must be 0-3")
        addr_bits = format(addr, "02b")
        return opcode + rs + addr_bits

    if instr == "LOADR":
        if len(parts) != 3:
            raise ValueError("LOADR expects a destination register and RAM address")
        opcode = OPCODES[instr]
        rd = parse_register(parts[1])
        addr = int(parts[2], 0)
        if addr < 0 or addr > 3:
            raise ValueError("RAM address must be 0-3")
        addr_bits = format(addr, "02b")
        return opcode + rd + addr_bits

    if instr == "HALT":
        return "11111111"

    raise ValueError(f"Unknown instruction: {instr}")


def assemble_program(program_text):
    machine_code = []
    for line_number, line in enumerate(program_text.splitlines(), start=1):
        try:
            instruction = assemble_line(line)
        except ValueError as exc:
            raise ValueError(f"Line {line_number}: {exc}") from exc

        if instruction is not None:
            machine_code.append(instruction)

    return machine_code


def to_logisim_hex(machine_code, rom_size=16):
    hex_values = [hex(int(binary, 2))[2:].zfill(2) for binary in machine_code]

    while len(hex_values) < rom_size:
        hex_values.append("ff")

    return "v2.0 raw\n" + " ".join(hex_values)


def save_hex_file(machine_code, filename="program.hex"):
    content = to_logisim_hex(machine_code)
    with open(filename, "w") as file:
        file.write(content)
    print(f"Saved to {filename}")
    print("\nHex output:")
    print(content)


program = """
LOAD R0 2
STORE R0 3
LOADR R1 3
"""


if __name__ == "__main__":
    machine_code = assemble_program(program)

    print("Machine Code:\n")
    for address, instruction in enumerate(machine_code):
        decimal = int(instruction, 2)
        print(f"{address}: {instruction}  (0x{decimal:02X})")

    print()
    print(machine_code)
    save_hex_file(machine_code)
