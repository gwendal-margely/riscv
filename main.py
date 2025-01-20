import argparse
from emulator import emu_loop, execute_instruction, decode_instruction
from cpu import RISCV_CPU
from memory import Memory
from peripherals import Peripherals

def main():
    default_livrable=read_livrable_prop()

    parser = argparse.ArgumentParser(description="Emulateur RISC-V")
    parser.add_argument("binary_file", type=str, help="Fichier binaire contenant les instructions RISC-V")
    parser.add_argument("--reset-addr", type=lambda x: int(x,0), default=0x100, help="Adresse de reset (défaut : 0x100)")
    parser.add_argument("--mem-size", type=lambda x: int(x,0), default=512*1024, help="Taille de la mémoire en octets (défaut : 512KB)")
    parser.add_argument("--step", action="store_true", help="Activer le mode pas à pas")
    parser.add_argument("--livrable", type=int, choices=[1, 2, 3, 4], default=default_livrable, help="Numéro du livrable à tester (défaut : 4)")
    args = parser.parse_args()

    cpu = RISCV_CPU()
    memory = Memory(args.mem_size)
    peripherals = Peripherals()
    memory.load_program(args.binary_file)
    cpu.set_pc(args.reset_addr)

    if args.livrable == 1:
        livrable_1(cpu, memory, args.step)
    elif args.livrable == 2:
        livrable_2(cpu, memory, args.step)
    elif args.livrable == 3:
        livrable_3(cpu, memory, peripherals, args.step)
    elif args.livrable == 4:
        livrable_4(cpu, memory, peripherals, args.step)


def read_livrable_prop():
    try:
        with open("livrable.prop", "r") as f:
            content = f.read().strip()
            if content in ["1", "2", "3", "4"]:
                return int(content)
            else:
                raise ValueError("Invalid value in livrable.prop")
    except (FileNotFoundError, ValueError):
        return 4  # Default value if file is not found or contains invalid value

def livrable_1(binary_file):
    with open(binary_file, "rb") as f, open("output.csv", "w", newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(["offset", "valeur", "opcode", "encoding"])
        offset = 0
        while chunk := f.read(4):
            if len(chunk) < 4:
                break
            inst = int.from_bytes(chunk, 'little')
            opcode = inst & 0x7F
            encoding = get_encoding(opcode)
            csvwriter.writerow([f"{offset:08x}", f"{inst:08x}", f"{opcode:08x}", encoding])
            offset += 4

def livrable_2(binary_file):
    with open(binary_file, "rb") as f:
        offset = 0
        while chunk := f.read(4):
            if len(chunk) < 4:
                break
            inst = int.from_bytes(chunk, 'little')
            disassembled_inst = decode_instruction(inst, mode=2)
            print(f"{offset:08x}: {disassembled_inst}")
            offset += 4

def livrable_3(cpu, memory, peripherals, step_by_step):
    emu_loop(cpu, memory, peripherals, step_by_step=step_by_step, enable_peripherals=False, enable_semihosting=False)

def livrable_4(cpu, memory, peripherals, step_by_step):
    emu_loop(cpu, memory, peripherals, step_by_step=step_by_step, enable_peripherals=True, enable_semihosting=True)

if __name__ == "__main__":
    main()