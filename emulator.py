from cpu import RISCV_CPU
from memory import Memory
from decoder import decode_instruction, sign_extend
from peripherals import Peripherals

# Fonctions spécifiques pour chaque type d'instruction
def execute_load(cpu, memory, inst):
    rd = (inst >> 7) & 0x1F
    rs1 = (inst >> 15) & 0x1F
    imm = sign_extend((inst >> 20) & 0xFFF, 12)
    addr = cpu.get_reg(rs1) + imm
    value = memory.read(addr, 4)  # Lecture de 4 octets (32 bits)
    cpu.set_reg(rd, value)

def execute_store(cpu, memory, inst):
    imm_11_5 = (inst >> 25) & 0x7F
    imm_4_0 = (inst >> 7) & 0x1F
    rs1 = (inst >> 15) & 0x1F
    rs2 = (inst >> 20) & 0x1F
    imm = sign_extend((imm_11_5 << 5) | imm_4_0, 12)
    addr = cpu.get_reg(rs1) + imm
    value = cpu.get_reg(rs2)
    memory.write(addr, value, 4)  # Écriture de 4 octets (32 bits)

def execute_branch(cpu, memory, inst):
    imm_12 = (inst >> 31) & 0x1
    imm_10_5 = (inst >> 25) & 0x3F
    imm_4_1 = (inst >> 8) & 0xF
    imm_11 = (inst >> 7) & 0x1
    rs1 = (inst >> 15) & 0x1F
    rs2 = (inst >> 20) & 0x1F
    imm = sign_extend((imm_12 << 12) | (imm_11 << 11) | (imm_10_5 << 5) | (imm_4_1 << 1), 13)
    if cpu.get_reg(rs1) == cpu.get_reg(rs2):
        cpu.set_pc(cpu.get_pc() + imm)
    else:
        cpu.set_pc(cpu.get_pc() + 4)

def execute_jalr(cpu, memory, inst):
    rd = (inst >> 7) & 0x1F
    rs1 = (inst >> 15) & 0x1F
    imm = sign_extend((inst >> 20) & 0xFFF, 12)
    next_pc = cpu.get_pc() + 4
    cpu.set_reg(rd, next_pc)
    cpu.set_pc(cpu.get_reg(rs1) + imm)

def execute_jal(cpu, memory, inst):
    rd = (inst >> 7) & 0x1F
    imm_20 = (inst >> 31) & 0x1
    imm_10_1 = (inst >> 21) & 0x3FF
    imm_11 = (inst >> 20) & 0x1
    imm_19_12 = (inst >> 12) & 0xFF
    imm = sign_extend((imm_20 << 20) | (imm_19_12 << 12) | (imm_11 << 11) | (imm_10_1 << 1), 21)
    next_pc = cpu.get_pc() + 4
    cpu.set_reg(rd, next_pc)
    cpu.set_pc(cpu.get_pc() + imm)

def execute_lui(cpu, memory, inst):
    rd = (inst >> 7) & 0x1F
    imm = (inst >> 12) & 0xFFFFF
    cpu.set_reg(rd, imm << 12)

def execute_auipc(cpu, memory, inst):
    rd = (inst >> 7) & 0x1F
    imm = (inst >> 12) & 0xFFFFF
    cpu.set_reg(rd, cpu.get_pc() + imm)

def execute_op_imm(cpu, memory, inst):
    rd = (inst >> 7) & 0x1F
    rs1 = (inst >> 15) & 0x1F
    imm = sign_extend((inst >> 20) & 0xFFF, 12)
    funct3 = (inst >> 12) & 0x7
    if funct3 == 0b000:  # ADDI
        cpu.set_reg(rd, cpu.get_reg(rs1) + imm)
    elif funct3 == 0b010:  # SLTI
        cpu.set_reg(rd, 1 if cpu.get_reg(rs1) < imm else 0)
    elif funct3 == 0b011:  # SLTIU
        cpu.set_reg(rd, 1 if cpu.get_reg(rs1) < imm else 0)
    elif funct3 == 0b100:  # XORI
        cpu.set_reg(rd, cpu.get_reg(rs1) ^ imm)
    elif funct3 == 0b110:  # ORI
        cpu.set_reg(rd, cpu.get_reg(rs1) | imm)
    elif funct3 == 0b111:  # ANDI
        cpu.set_reg(rd, cpu.get_reg(rs1) & imm)
    elif funct3 == 0b001:  # SLLI
        cpu.set_reg(rd, cpu.get_reg(rs1) << imm)
    elif funct3 == 0b101:  # SRLI/SRAI
        funct7 = (inst >> 25) & 0x7F
        if funct7 == 0b0000000:  # SRLI
            cpu.set_reg(rd, cpu.get_reg(rs1) >> imm)
        elif funct7 == 0b0100000:  # SRAI
            cpu.set_reg(rd, (cpu.get_reg(rs1) >> imm) | ((cpu.get_reg(rs1) & (1 << (32 - imm))) >> (32 - imm)))

def execute_op(cpu, memory, inst):
    rd = (inst >> 7) & 0x1F
    rs1 = (inst >> 15) & 0x1F
    rs2 = (inst >> 20) & 0x1F
    funct3 = (inst >> 12) & 0x7
    if funct3 == 0b000:  # ADD/SUB
        funct7 = (inst >> 25) & 0x7F
        if funct7 == 0b0000000:  # ADD
            cpu.set_reg(rd, cpu.get_reg(rs1) + cpu.get_reg(rs2))
        elif funct7 == 0b0100000:  # SUB
            cpu.set_reg(rd, cpu.get_reg(rs1) - cpu.get_reg(rs2))
    elif funct3 == 0b001:  # SLL
        cpu.set_reg(rd, cpu.get_reg(rs1) << cpu.get_reg(rs2))
    elif funct3 == 0b010:  # SLT
        cpu.set_reg(rd, 1 if cpu.get_reg(rs1) < cpu.get_reg(rs2) else 0)
    elif funct3 == 0b011:  # SLTU
        cpu.set_reg(rd, 1 if cpu.get_reg(rs1) < cpu.get_reg(rs2) else 0)
    elif funct3 == 0b100:  # XOR
        cpu.set_reg(rd, cpu.get_reg(rs1) ^ cpu.get_reg(rs2))
    elif funct3 == 0b101:  # SRL/SRA
        funct7 = (inst >> 25) & 0x7F
        if funct7 == 0b0000000:  # SRL
            cpu.set_reg(rd, cpu.get_reg(rs1) >> cpu.get_reg(rs2))
        elif funct7 == 0b0100000:  # SRA
            cpu.set_reg(rd, (cpu.get_reg(rs1) >> cpu.get_reg(rs2)) | ((cpu.get_reg(rs1) & (1 << (32 - cpu.get_reg(rs2)))) >> (32 - cpu.get_reg(rs2))))
    elif funct3 == 0b110:  # OR
        cpu.set_reg(rd, cpu.get_reg(rs1) | cpu.get_reg(rs2))
    elif funct3 == 0b111:  # AND
        cpu.set_reg(rd, cpu.get_reg(rs1) & cpu.get_reg(rs2))

def execute_system(cpu, memory, inst):
    funct3 = (inst >> 12) & 0x7
    if funct3 == 0b000:  # ECALL/EBREAK
        imm = (inst >> 20) & 0xFFF
        if imm == 0b000000000000:  # ECALL
            pass  # Rien à faire pour ECALL
        elif imm == 0b000000000001:  # EBREAK
            print("EBREAK détecté")

def execute_instruction(cpu, memory, inst, peripherals, enable_peripherals, enable_semihosting):
    opcode = inst & 0x7F  # Les 7 bits de poids faible
    if opcode == 0b0000011:  # LOAD
        execute_load(cpu, memory, inst)
    elif opcode == 0b0100011:  # STORE
        execute_store(cpu, memory, inst)
    elif opcode == 0b1100011:  # BRANCH
        execute_branch(cpu, memory, inst)
    elif opcode == 0b1100111:  # JALR
        execute_jalr(cpu, memory, inst)
    elif opcode == 0b1101111:  # JAL
        execute_jal(cpu, memory, inst)
    elif opcode == 0b0110111:  # LUI
        execute_lui(cpu, memory, inst)
    elif opcode == 0b0010111:  # AUIPC
        execute_auipc(cpu, memory, inst)
    elif opcode == 0b0010011:  # OP_IMM
        execute_op_imm(cpu, memory, inst)
    elif opcode == 0b0110011:  # OP
        execute_op(cpu, memory, inst)
    elif opcode == 0b1110011:  # SYSTEM
        execute_system(cpu, memory, inst)
    else:
        print("Instruction inconnue")

    # Gérer les accès mémoire aux périphériques
    address = cpu.get_pc()
    if enable_peripherals and peripherals.handle_memory_access(address, inst, is_write=True) is not None:
        return
    if enable_peripherals and peripherals.handle_memory_access(address, inst, is_write=False) is not None:
        return

    # Gérer le semihosting
    if enable_semihosting and inst == 0x00100073:  # ebreak
        if cpu.get_reg(10) == 0x04:  # SYS_WRITEC
            peripherals.write_stdout(cpu.get_reg(11))
        elif cpu.get_reg(10) == 0x06:  # SYS_WRITE0
            string = ""
            addr = cpu.get_reg(11)
            while memory.read(addr, 1) != 0:
                string += chr(memory.read(addr, 1))
                addr += 1
            print(string, end='', flush=True)

def emu_loop(cpu, memory, peripherals, step_by_step=False, enable_peripherals=True, enable_semihosting=True):
    result_stack = []
    while True:
        try:
            inst = memory.read(cpu.get_pc(), 4)
            if step_by_step:
                print(f"PC: {cpu.get_pc():#x}, Instruction: {decode_instruction(inst, mode=2)}")
                command = input("Commande (step/continue/exit/x/COUNT ADDRESS/reset): ")
                if command == "step":
                    result = execute_instruction(cpu, memory, inst, peripherals, enable_peripherals, enable_semihosting)
                    result_stack.append(result)
                    cpu.set_pc(cpu.get_pc() + 4)
                elif command == "continue":
                    step_by_step = False
                elif command == "exit":
                    break
                else:
                    handle_command(command, cpu, memory)
            else:
                result = execute_instruction(cpu, memory, inst, peripherals, enable_peripherals, enable_semihosting)
                result_stack.append(result)
                cpu.set_pc(cpu.get_pc() + 4)
        except MemoryError as e:
            print(f"Erreur : {e}")
            step_by_step = True
    return result_stack

def handle_command(command, cpu, memory):
    parts = command.split()
    if parts[0] == "x":
        count = int(parts[1].split('/')[0])
        address = int(parts[1].split('/')[1], 16)
        for i in range(count):
            value = memory.read(address + i, 1)
            print(f"{address + i:08x}: {value:02x}")
    elif parts[0] == "reset":
        cpu.set_pc(0x100)  # Reset address
    elif parts[0] == "continue":
        return False
    elif parts[0] == "exit":
        return True
    return True
