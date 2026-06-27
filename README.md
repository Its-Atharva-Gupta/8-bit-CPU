# 8-Bit CPU (Logisim)

A fully functional **8-bit CPU** designed and simulated in [Logisim](http://www.cburch.com/logisim/), complete with a custom **assembler** that compiles assembly code into machine code ready to load into the circuit's ROM.

Built as a digital logic project to explore computer architecture fundamentals — from individual gates up through ALU, registers, RAM, control logic, and program execution.

---

## Repository Structure

| File | Description |
|---|---|
| `FullAdder.circ` | Full Logisim circuit file containing the entire CPU — from basic gates to the top-level datapath |
| `assembler.py` | Python assembler that translates assembly mnemonics into 8-bit machine code and outputs Logisim-compatible `.hex` files |
| `program.hex` | Sample assembled program ready for ROM loading in Logisim |
| `image.png` | Screenshot of the Logisim circuit |

---

## Architecture

### Datapath Components

| Component | Description |
|---|---|
| **FullAdder** | 1-bit full adder (building block of the ALU) |
| **Adder_8_bit** | 8-bit ripple-carry adder |
| **AND_8_bit / OR_8_bit / XOR_8_bit** | 8-bit bitwise logic units |
| **NOT Gate, NAND Gate, NOR Gate** | Basic logic for control and glue logic |
| **SR_Latch** | Set-Reset latch used in control sequencing |
| **D Flip-Flop** | Edge-triggered storage elements |
| **Decoder_2to4** | 2-to-4 line decoder (register select, RAM addressing) |
| **MUX_4to1** | 4-to-1 multiplexer |
| **MUX_8_bit_4_to_1** | 8-bit wide 4-to-1 multiplexer (ALU source selection) |
| **My_Multiplexer** | Custom multiplexer subcircuit |
| **Register8** | 8-bit register (CPU registers R0–R3) |
| **Program_Counter** | Program counter with load/enable control |
| **RAM4x8** | 4-word × 8-bit RAM for data memory |
| **Clock** | System clock driving execution |
| **Constant** | Constant value generators |
| **DipSwitch / Button** | Manual input / reset / step controls |
| **Pin / Ground / LED** | I/O, power, and visual output indicators |

### Instruction Set

All instructions are **8 bits wide**. The assembler (`assembler.py`) supports:

| Mnemonic | Opcode | Operands | Description |
|---|---|---|---|
| `ADD` | `0000` | `Rd, Rs` | `Rd ← Rd + Rs` |
| `SUB` | `0001` | `Rd, Rs` | `Rd ← Rd - Rs` |
| `AND` | `0010` | `Rd, Rs` | `Rd ← Rd & Rs` |
| `OR` | `0011` | `Rd, Rs` | `Rd ← Rd \| Rs` |
| `XOR` | `0100` | `Rd, Rs` | `Rd ← Rd ⊕ Rs` |
| `LOAD` | `0101` | `Rd, Imm` | `Rd ← Immediate (0–3)` |
| `JUMP` | `0110` | `Addr` | `PC ← Address (0–15)` |
| `JZ` | `0111` | `Addr` | `PC ← Address if Zero flag set` |
| `STORE` | `1000` | `Rs, Addr` | `RAM[Addr] ← Rs` |
| `LOADR` | `1001` | `Rd, Addr` | `Rd ← RAM[Addr]` |
| `MOV` | `1110` | `Rd, Rs` | `Rd ← Rs` |
| `HALT` | `1111` | — | `Halt execution` |

**Registers:** R0 (`00`), R1 (`01`), R2 (`10`), R3 (`11`)

---

## Getting Started

### Prerequisites

- [Logisim](http://www.cburch.com/logisim/download.html) (version 2.7.x recommended)
- Python 3 (for the assembler)

### Running the Simulation

1. Open `FullAdder.circ` in Logisim.
2. Navigate to the **main** circuit (top-level).
3. Load a program into the ROM:
   - Right-click the ROM component → **Load Image...** → select `program.hex`.
4. Enable simulation (Simulate → Ticks Enabled, or press Ctrl+T).
5. Use the **Clock** to step through execution. Observe register values, RAM contents, and the program counter via the **LED** indicators and probes.

### Using the Assembler

```bash
python3 assembler.py
```

Edit the `program` variable at the bottom of `assembler.py` to write your own program:

```python
program = """
LOAD R0 2      # R0 = 2
STORE R0 3     # RAM[3] = R0
LOADR R1 3     # R1 = RAM[3]
"""
```

The assembler outputs:
- A console log of the assembled machine code with addresses
- A `program.hex` file in Logisim's `v2.0 raw` format, automatically padded to 16 ROM words (unused slots are `0xFF` = HALT)

---

## Example Program

**Assembly:**
```asm
LOAD R0 2       # R0 ← 2
STORE R0 3      # RAM[3] ← R0
LOADR R1 3      # R1 ← RAM[3]  → R1 = 2
```

**Machine code (hex):**
```
52 83 97 ff ff ff ff ff ff ff ff ff ff ff ff ff
```

| Address | Binary | Hex | Instruction |
|---|---|---|---|
| 0 | `0101 0010` | `0x52` | `LOAD R0 2` |
| 1 | `1000 0011` | `0x83` | `STORE R0 3` |
| 2 | `1001 0111` | `0x97` | `LOADR R1 3` |
| 3–15 | `1111 1111` | `0xFF` | `HALT` (padding) |

---

## Build Notes

- The project was built incrementally: logic gates → FullAdder → 8-bit ALU → register file → program counter → RAM → control unit → final datapath integration.
- `.agents/` and `.codex/` directories are IDE/agent workspace metadata and can be ignored.

---

## License

This project is open source. Feel free to use, modify, and extend it for learning or teaching digital logic and computer architecture.
