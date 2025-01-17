import argparse
from emulator import emu_loop, execute_instruction, decode_instruction
from cpu import RISCV_CPU
from memory import Memory
from peripherals import Peripherals

def main():
    parser = argparse.ArgumentParser(description="Emulateur RISC-V")
    parser.add_argument("binary_file", type=str, help="Fichier binaire contenant les instructions RISC-V")
    parser.add_argument("--reset-addr", type=lambda x: int(x,0), default=0x100, help="Adresse de reset (défaut : 0x100)")
    parser.add_argument("--mem-size", type=lambda x: int(x,0), default=512*1024, help="Taille de la mémoire en octets (défaut : 512KB)")
    parser.add_argument("--step", action="store_true", help="Activer le mode pas à pas")
    parser.add_argument("--livrable", type=int, choices=[1, 2, 3, 4], default=4, help="Numéro du livrable à tester (défaut : 4)")
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

def livrable_1(cpu, memory, step_by_step):
    while True:
        try:
            inst = memory.read(cpu.get_pc(), 4)
            if step_by_step:
                print(f"PC: {cpu.get_pc():#x}, Instruction: {decode_instruction(inst, mode=1)}")
                command = input("Commande (step/continue/exit): ")
                if command == "step":
                    cpu.set_pc(cpu.get_pc() + 4)
                elif command == "continue":
                    step_by_step = False
                elif command == "exit":
                    break
            else:
                cpu.set_pc(cpu.get_pc() + 4)
        except MemoryError as e:
            print(f"Erreur : {e}")
            step_by_step = True

def livrable_2(cpu, memory, step_by_step):
    while True:
        try:
            inst = memory.read(cpu.get_pc(), 4)
            if step_by_step:
                print(f"PC: {cpu.get_pc():#x}, Instruction: {decode_instruction(inst, mode=2)}")
                command = input("Commande (step/continue/exit): ")
                if command == "step":
                    cpu.set_pc(cpu.get_pc() + 4)
                elif command == "continue":
                    step_by_step = False
                elif command == "exit":
                    break
            else:
                cpu.set_pc(cpu.get_pc() + 4)
        except MemoryError as e:
            print(f"Erreur : {e}")
            step_by_step = True

def livrable_3(cpu, memory, peripherals, step_by_step):
    emu_loop(cpu, memory, peripherals, step_by_step=step_by_step, enable_peripherals=False, enable_semihosting=False)

def livrable_4(cpu, memory, peripherals, step_by_step):
    emu_loop(cpu, memory, peripherals, step_by_step=step_by_step, enable_peripherals=True, enable_semihosting=True)

if __name__ == "__main__":
    main()