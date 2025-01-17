class Memory:
    def __init__(self, size):
        self.size = size
        self.mem = bytearray(size)

    def load_program(self, binary_file):
        with open(binary_file, "rb") as f:
            self.mem[:len(f.read())] = f.read()

    def read(self, address, size):
        if address + size > self.size:
            raise MemoryError("Adresse invalide")
        return int.from_bytes(self.mem[address:address+size], 'little')

    def write(self, address, value, size):
        if address + size > self.size:
            raise MemoryError("Adresse invalide")
        self.mem[address:address+size] = value.to_bytes(size, 'little')
