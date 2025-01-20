.section .data
hello_str:
    .asciz "Hello, World!\n"

.section .text
.globl _start
_start:
    # Charger l'adresse de la chaîne "Hello, World!\n" dans a0 (x10)
    la a0, hello_str
    
    # Appel semihosting pour afficher la chaîne
    li a7, 64  # a7 = 64 (SYS_WRITE0)
    ecall
    
    # Terminer le programme
    li a7, 93  # a7 = 93 (EXIT)
    ecall
