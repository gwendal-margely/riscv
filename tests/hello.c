#define STDOUT_ADDR 0x4000004
#define STDERR_ADDR 0x4000008
#define STDIN_ADDR  0x4000000

void write_stdout(char c) {
    volatile unsigned int *stdout_ptr = (unsigned int *)STDOUT_ADDR;
    *stdout_ptr = c;
}

void write_stderr(char c) {
    volatile unsigned int *stderr_ptr = (unsigned int *)STDERR_ADDR;
    *stderr_ptr = c;
}

char read_stdin() {
    volatile unsigned int *stdin_ptr = (unsigned int *)STDIN_ADDR;
    return (char)*stdin_ptr;
}

//Point d'entree pour le compilateur RISCV ELF GCC en mode -nostdlib -nostartfiles
void _start() {
    int main();
    main();
    while (1);
}

int main() {
    // Écrire "Hello World !" sur la sortie standard
    char *hello_world = "Hello World !";
    for (int i = 0; hello_world[i] != '\0'; i++) {
        write_stdout(hello_world[i]);
    }

    // Écrire "Errooorrrr ?????" sur la sortie d'erreur
    char *error_message = "Errooorrrr ?????";
    for (int i = 0; error_message[i] != '\0'; i++) {
        write_stderr(error_message[i]);
    }

    // Lire un caractère depuis l'entrée standard
    char input_char = read_stdin();

    // Écrire le caractère lu sur la sortie standard
    write_stdout(input_char);

    return 0;
}