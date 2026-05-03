# Hack Assembler

A Hack assembler built in Python that runs on your terminal. 
It takes a Hack Assembly (.asm) file as input and produces 
the equivalent 16-bit binary machine code (.hack) file.

## Usage
python assembler.py <filename.asm>


## Example
python assembler.py Fill.asm


This will produce `Fill.hack` in the same folder.

## Features
- Translates A instructions (@value) to 16-bit binary
- Translates C instructions (dest=comp;jump) to 16-bit binary
- Handles labels (LOOP), variables (@i), and predefined symbols (@KBD, @SCREEN, @R0 etc.)
- Two-pass assembly for symbol resolution
- Auto-generates output .hack file in same folder as input

## How it works
**Pass 1** — Scans the .asm file and builds a symbol table of all labels and their addresses.

**Pass 2** — Translates each instruction to binary, replacing symbols with their addresses from the symbol table.

## Predefined Symbols Supported
| Symbol | Value |
|--------|-------|
| R0-R15 | 0-15 |
| SCREEN | 16384 |
| KBD | 24576 |
| SP | 0 |
| LCL | 1 |
| ARG | 2 |
| THIS | 3 |
| THAT | 4 |

## Requirements
- Python 3.x

## What is Hack Assembly?
Hack Assembly is the assembly language for the Hack computer — 
a simple 16-bit computer. It has two types of instructions:
- **A instruction** → `@value` (loads a value into the A register)
- **C instruction** → `dest=comp;jump` (performs computation)
