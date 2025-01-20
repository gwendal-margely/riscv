# decoder.py

import struct
import csv

# opcodes pour les différents types d'instructions RV32I
OPCODES = {
    "LOAD": 0b0000011,
    "STORE": 0b0100011,
    "BRANCH": 0b1100011,
    "JALR": 0b1100111,
    "JAL": 0b1101111,
    "LUI": 0b0110111,
    "AUIPC": 0b0010111,
    "OP_IMM": 0b0010011,
    "OP": 0b0110011,
    "SYSTEM": 0b1110011,
}

def generate_csv(cpu, memory):
    with open('output.csv', 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(["offset", "valeur", "opcode", "encoding"])
        pc = cpu.get_pc()
        while pc < memory.size:
            inst = memory.read(pc, 4)
            opcode = inst & 0x7F
            encoding = get_encoding(opcode)
            csvwriter.writerow([f"{pc:08x}", f"{inst:08x}", f"{opcode:08x}", encoding])
            pc += 4

def get_encoding(opcode):
    encoding_map = {
        0b0000011: "I",
        0b0100011: "S",
        0b1100011: "S_B",
        0b1100111: "I",
        0b1101111: "U_J",
        0b0110111: "U",
        0b0010111: "U",
        0b0010011: "I",
        0b0110011: "R",
        0b1110011: "I"
    }
    return encoding_map.get(opcode, "Unknown")

# Fonction pour décoder une instruction RV32I
def decode_instruction(inst, mode=2):
    """
    Décode une instruction binaire de 32 bits en fonction du type RV32I.
    Arguments :
        inst : int (32 bits) représentant une instruction RV32I
        mode : int (1 ou 2), pour choisir le niveau de détail (simplifié ou complet)
    Retourne :
        Une chaîne de caractère décrivant l'instruction assembleur
    """
    opcode = inst & 0x7F  # Les 7 bits de poids faible

    if mode == 1:  # Décodage simplifié (Livrable 1)
        return f"Opcode {opcode:#x} (simplifié)"
    
    # Décodage complet (Livrable 2)
    if opcode == OPCODES["LOAD"]:
        return decode_load(inst)
    elif opcode == OPCODES["STORE"]:
        return decode_store(inst)
    elif opcode == OPCODES["BRANCH"]:
        return decode_branch(inst)
    elif opcode == OPCODES["JALR"]:
        return decode_jalr(inst)
    elif opcode == OPCODES["JAL"]:
        return decode_jal(inst)
    elif opcode == OPCODES["LUI"]:
        return decode_lui(inst)
    elif opcode == OPCODES["AUIPC"]:
        return decode_auipc(inst)
    elif opcode == OPCODES["OP_IMM"]:
        return decode_op_imm(inst)
    elif opcode == OPCODES["OP"]:
        return decode_op(inst)
    elif opcode == OPCODES["SYSTEM"]:
        return decode_system(inst)
    else:
        return "Instruction inconnue"

# Fonctions spécifiques pour chaque type d'instruction
def decode_load(inst):
    rd = (inst >> 7) & 0x1F
    rs1 = (inst >> 15) & 0x1F
    imm = sign_extend((inst >> 20) & 0xFFF, 12)
    return f"LOAD x{rd}, {imm}(x{rs1})"

def decode_store(inst):
    imm_11_5 = (inst >> 25) & 0x7F
    imm_4_0 = (inst >> 7) & 0x1F
    rs1 = (inst >> 15) & 0x1F
    rs2 = (inst >> 20) & 0x1F
    imm = sign_extend((imm_11_5 << 5) | imm_4_0, 12)
    return f"STORE x{rs2}, {imm}(x{rs1})"

def decode_branch(inst):
    imm_12 = (inst >> 31) & 0x1
    imm_10_5 = (inst >> 25) & 0x3F
    imm_4_1 = (inst >> 8) & 0xF
    imm_11 = (inst >> 7) & 0x1
    rs1 = (inst >> 15) & 0x1F
    rs2 = (inst >> 20) & 0x1F
    imm = sign_extend((imm_12 << 12) | (imm_11 << 11) | (imm_10_5 << 5) | (imm_4_1 << 1), 13)
    return f"BRANCH x{rs1}, x{rs2}, {imm}"

def decode_jalr(inst):
    rd = (inst >> 7) & 0x1F
    rs1 = (inst >> 15) & 0x1F
    imm = sign_extend((inst >> 20) & 0xFFF, 12)
    return f"JALR x{rd}, {imm}(x{rs1})"

def decode_jal(inst):
    rd = (inst >> 7) & 0x1F
    imm_20 = (inst >> 31) & 0x1
    imm_10_1 = (inst >> 21) & 0x3FF
    imm_11 = (inst >> 20) & 0x1
    imm_19_12 = (inst >> 12) & 0xFF
    imm = sign_extend((imm_20 << 20) | (imm_19_12 << 12) | (imm_11 << 11) | (imm_10_1 << 1), 21)
    return f"JAL x{rd}, {imm}"

def decode_lui(inst):
    rd = (inst >> 7) & 0x1F
    imm = (inst >> 12) & 0xFFFFF
    return f"LUI x{rd}, {imm}"

def decode_auipc(inst):
    rd = (inst >> 7) & 0x1F
    imm = (inst >> 12) & 0xFFFFF
    return f"AUIPC x{rd}, {imm}"

def decode_op_imm(inst):
    rd = (inst >> 7) & 0x1F
    rs1 = (inst >> 15) & 0x1F
    imm = sign_extend((inst >> 20) & 0xFFF, 12)
    return f"OP_IMM x{rd}, x{rs1}, {imm}"

def decode_op(inst):
    rd = (inst >> 7) & 0x1F
    rs1 = (inst >> 15) & 0x1F
    rs2 = (inst >> 20) & 0x1F
    return f"OP x{rd}, x{rs1}, x{rs2}"

def decode_system(inst):
    return "SYSTEM Instruction"

def sign_extend(value, bits):
    """Étend le bit de signe de la valeur donnée."""
    if (value & (1 << (bits - 1))) != 0:
        value -= (1 << bits)
    return value