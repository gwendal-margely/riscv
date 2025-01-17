riscv64-unknown-elf-as -o hello_world.o hello_world.s
riscv64-unknown-elf-ld -o hello_world.bin hello_world.o
rm -rf hello_world.o
mv hello_world.bin bin/