from cpu import RISCV_CPU
from memory import Memory
from peripherals import Peripherals
from decoder import decode_instruction, sign_extend

# Structure pour la mémoire commune de l'ordonnancement
class ReorderBuffer:
    def __init__(self):
        self.buffer = []

    def add_instruction(self, inst):
        self.buffer.append(inst)

    def commit_instruction(self):
        if self.buffer:
            return self.buffer.pop(0)
        return None

    def is_empty(self):
        return len(self.buffer) == 0

def setup_ooo(cpu, memory, peripherals):
    cpu.rob = ReorderBuffer()

# Fonction pour réordonner les instructions avant l'exécution
def reorder_instructions(cpu, memory):

    binary_file = memory.mem
    instructions = []
    for i in range(0, len(binary_file), 4):
        inst = int.from_bytes(binary_file[i:i+4], 'little')
        instructions.append(inst)

    # Réordonner les instructions
    reordered_instructions = reorder_logic(instructions)

    for i, inst in enumerate(reordered_instructions):
        memory.write(i * 4, inst, 4)

    for inst in reordered_instructions:
        cpu.rob.add_instruction(inst)

def reorder_results(cpu, memory, result_stack):

    reordered_results = []
    while not cpu.rob.is_empty():
        inst = cpu.rob.commit_instruction()
        result = result_stack.pop(0)
        reordered_results.append(result)

    return reordered_results

# Fonction pour réordonner les instructions en fonction de leur type et de leurs dépendances
def reorder_logic(instructions):

    dependencies = {}
    independent_instructions = []

    for i, inst in enumerate(instructions):
        opcode = inst & 0x7F
        if opcode in [0b0000011, 0b0100011, 0b1100011, 0b1100111, 0b1101111, 0b0110111, 0b0010111, 0b0010011, 0b0110011, 0b1110011]:
            # Instructions dépendantes
            dependencies[i] = []
        else:
            # Instructions indépendantes
            independent_instructions.append(i)

    reordered_instructions = [instructions[i] for i in independent_instructions]

    while dependencies:
        for i, deps in list(dependencies.items()):
            if all(dep in reordered_instructions for dep in deps):
                reordered_instructions.append(instructions[i])
                del dependencies[i]

    return reordered_instructions