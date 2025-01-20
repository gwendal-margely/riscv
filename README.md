# Emulateur RISC-V

## Description du Projet

Ce projet consiste à développer un émulateur de processeur RISC-V en utilisant Python. L'émulateur permet de décoder, désassembler et exécuter des instructions RISC-V à partir de fichiers binaires. Le projet est divisé en quatre livrables, chacun ajoutant des fonctionnalités spécifiques à l'émulateur. 

## Spécifications du Projet

### Livrable 1 : Un premier décodeur

**Objectif :**
Écrire un programme qui prend en paramètre un chemin vers un fichier binaire, extrait les 7 bits d'opcode de chaque mot de 32 bits, déduit le type d'instruction et le type d'encodage utilisé.

**Sortie attendue :**
Format CSV avec les colonnes : offset, valeur, opcode, encoding.

---
### Livrable 2 : Un désassembleur complet

**Objectif :**
Écrire un programme qui désassemble un fichier contenant des instructions au format binaire et affiche les instructions en langage assembleur.

**Sortie attendue :**
Affichage sur la sortie standard, contenant une instruction complètement décodée par ligne.

---

### Livrable 3 : Un émulateur sans entrées/sortie

**Objectif :**
Écrire un programme qui crée un processeur et une mémoire, charge un fichier binaire, initialise le registre pc, et démarre l'exécution des instructions.

**Fonctionnalités attendues :**
- Choix de la taille de mémoire et de l'adresse de reset sur la ligne de commande. (defaut 512 KB)
- Exécution pas à pas avec affichage des registres et du registre pc. (paramètre --step)
- Support des commandes : step, x/COUNT ADDRESS, reset, continue, exit.
- Gestion des erreurs sans arrêt inattendu de l'émulateur.

---

### Livrable 4 : Interactions avec le monde extérieur

**Objectif :**
Ajouter des périphériques d'entrée/sortie et supporter le semihosting.

**Fonctionnalités attendues :**
- Périphériques pour envoyer des octets sur la sortie standard et d'erreur.
- Périphérique pour lire un octet depuis l'entrée standard.
- Support du semihosting pour des opérations comme SYS_WRITEC et SYS_WRITE0.

## Guide d'Installation

### Prérequis

- Python 3.x
- Les bibliothèques standard de Python

### Installation

1. **Cloner le dépôt :**
   ```bash
   git clone https://https://github.com/gwendal-margely/riscv
   cd riscv
   ```

2. **Installer les dépendances :**
   ```bash
   pip install -r requirements.txt
   ```

## Utilisation

### Utilisation Générale

L'émulateur peut être utilisé en spécifiant le livrable à tester et le fichier binaire contenant les instructions RISC-V.

```bash
python main.py path/to/binary_file.bin --livrable <livrable_number> [--step]
```

- `path/to/binary_file.bin` : Chemin vers le fichier binaire contenant les instructions RISC-V.
- `--livrable <livrable_number>` : Numéro du livrable à tester (1, 2, 3 ou 4).
- `--step` : Activer le mode pas à pas (optionnel).

### Utilisation des Livrables

#### Livrable 1

Pour utiliser le décodeur d'instructions :

```bash
python main.py path/to/binary_file.bin --livrable 1
```

Cela générera un fichier CSV contenant les informations de décodage des instructions.

#### Livrable 2

Pour utiliser le désassembleur :

```bash
python main.py path/to/binary_file.bin --livrable 2
```

Cela affichera les instructions désassemblées sur la sortie standard.

#### Livrable 3

Pour utiliser l'émulateur sans entrées/sorties :

```bash
python main.py path/to/binary_file.bin --livrable 3
```

Cela exécutera les instructions, affichant les registres et le compteur de programme.

#### Livrable 4

Pour utiliser l'émulateur complet avec entrées/sorties :

```bash
python main.py path/to/binary_file.bin --livrable 4
```

Cela exécutera les instructions, affichant les registres et le compteur de programme, et permettra les interactions avec les périphériques et le semihosting.

---

## Options :

``` bash
python main.py <binary-file-path> [--livrable <numero-livrable>] [--mem-size <mem-size-in-bytes>] [--reset-addr <addr>] [--step]
```

### --reset-addr

* Adresse de reset *(défaut : 0x100)*

### --mem-size

* Taille de la mémoire en octets *(défaut : 512KB)*

### --livrable

* Numéro du livrable à tester *[1 à 4]*

### --step

* mode pas-à-pas *(défaut : false)*

---

## Avec Docker :

### Livrable 1 : Decodeur

``` bash
docker build -t decoder -f livrables/Dockerfile.l1 .
docker run --rm -v $(pwd):/data decoder
```

### Livrable 2 : Désassembleur

``` bash
docker build -t disassembler -f livrables/Dockerfile.l2 .
docker run --rm -v $(pwd):/data disassembler
```

### Livrable 3 : Emulateur (sans Entrée/Sortie)

``` bash
docker build -t riscv-emulator-l3 -f livrables/Dockerfile.l3 .
docker run --rm -v $(pwd):/data riscv-emulator-l3
```

### Livrable 4 : Emulateur (avec Entrée/Sortie)

``` bash
docker build -t riscv-emulator-l4 -f livrables/Dockerfile.l4 .
docker run --rm -v $(pwd):/data riscv-emulator-l4
```