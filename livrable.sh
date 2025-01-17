#!/bin/bash

# Vérifie si un paramètre est passé
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <livrable>"
    echo "livrable: 1, 2, 3 ou 4"
    exit 1
fi

LIVRABLE=$1

# Vérifie si le paramètre est valide
if [ "$LIVRABLE" -ne 1 ] && [ "$LIVRABLE" -ne 2 ] && [ "$LIVRABLE" -ne 3 ] && [ "$LIVRABLE" -ne 4 ]; then
    echo "Paramètre invalide. Utilisez 1, 2, 3 ou 4."
    exit 1
fi

# Construit et exécute le Dockerfile correspondant
case $LIVRABLE in
    1)
        docker build -t riscv_emulator_l1 -f livrables/Dockerfile.l1 .
        docker run --rm -v $(pwd):/data riscv_emulator_l1
        ;;
    2)
        docker build -t riscv_emulator_l2 -f livrables/Dockerfile.l2 .
        docker run --rm -v $(pwd):/data riscv_emulator_l2
        ;;
    3)
        docker build -t riscv_emulator_l3 -f livrables/Dockerfile.l3 .
        docker run --rm -v $(pwd):/data riscv_emulator_l3
        ;;
    4)
        docker build -t riscv_emulator_l4 -f livrables/Dockerfile.l4 .
        docker run --rm -v $(pwd):/data riscv_emulator_l4
        ;;
esac
