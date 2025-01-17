class RISCV_CPU:
    def __init__(self):
        self.regs = [0] * 32  # 32 registres de 32 bits
        self.pc = 0  # Compteur de programme

    def set_pc(self, address):
        self.pc = address

    def get_pc(self):
        return self.pc

    def set_reg(self, index, value):
        if index == 0:
            return  # x0 est toujours 0
        self.regs[index] = value

    def get_reg(self, index):
        if index == 0:
            return 0  # x0 est toujours 0
        return self.regs[index]
