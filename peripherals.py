import sys


class Peripherals:
    def __init__(self):
        self.stdout_addr = 0x4000004
        self.stderr_addr = 0x4000008
        self.stdin_addr = 0x4000000

    def write_stdout(self, value):
        print(chr(value & 0xFF), end='', flush=True)

    def write_stderr(self, value):
        print(chr(value & 0xFF), end='', flush=True, file=sys.stderr)

    def read_stdin(self):
        return ord(input("Entrée : ")[0])

    def handle_memory_access(self, address, value, is_write):
        if address == self.stdout_addr and is_write:
            self.write_stdout(value)
        elif address == self.stderr_addr and is_write:
            self.write_stderr(value)
        elif address == self.stdin_addr and not is_write:
            return self.read_stdin()
        return None