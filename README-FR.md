# Convertisseur d’entiers avec Python et Docker

Ce petit projet convertit un entier décimal en représentation binaire et hexadécimale. Pour les nombres négatifs, il utilise le complément à deux.

Le programme choisit automatiquement la largeur signée minimale adaptée à la valeur : 8, 16, 32 ou 64 bits.

## Exemples

```text
$ convert 127
Décimal     : 127
Binaire     : 0111 1111
Hexadécimal : 0x7F  (7F)
```

```text
$ convert -129
Décimal     : -129
Binaire     : 1111 1111 0111 1111
Hexadécimal : 0xFF7F  (FF 7F)
```

## Structure du projet

```text
.
├── convert.py
├── Dockerfile
└── README.md
```

## Fonctionnement du programme Python

### Choix de la largeur

La fonction `choose_width()` détermine le plus petit type entier signé capable de contenir la valeur :

```python
def choose_width(n):
    if -128 <= n <= 127:
        return 8
    if -32768 <= n <= 32767:
        return 16
    if -2147483648 <= n <= 2147483647:
        return 32
    return 64
```

| Largeur | Type C/C++ | Valeurs signées |
|---:|---|---:|
| 8 bits | `int8_t` | -128 à 127 |
| 16 bits | `int16_t` | -32 768 à 32 767 |
| 32 bits | `int32_t` | -2 147 483 648 à 2 147 483 647 |
| 64 bits | `int64_t` | -9 223 372 036 854 775 808 à 9 223 372 036 854 775 807 |

### Complément à deux

Python utilise des entiers de taille variable. Pour obtenir une représentation finie en complément à deux, le programme applique un masque correspondant à la largeur choisie :

```python
mask = (1 << total_bits) - 1
value = n & mask
```

Par exemple, `-128` sur 8 bits devient :

```text
1000 0000
```

### Affichage binaire

La représentation binaire est complétée avec des zéros à gauche, puis regroupée par blocs de quatre bits :

```python
bits = format(n & mask, f"0{total_bits}b")
```

### Affichage hexadécimal

Le nombre de chiffres hexadécimaux dépend de la largeur choisie :

```python
hex_digits = total_bits // 4
hexa = format(n & mask, f"0{hex_digits}X")
```

L’affichage est regroupé par octets, soit deux caractères hexadécimaux :

```text
0x3E7E  (3E 7E)
```

## Dockerfile

```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY convert.py .

ENTRYPOINT ["python", "convert.py"]
```

L’instruction `ENTRYPOINT` fixe la commande exécutée dans le conteneur. Tout argument placé après le nom de l’image est ajouté à cette commande.

Ainsi :

```bash
docker run --rm convert 15998
```

équivaut, dans le conteneur, à :

```bash
python convert.py 15998
```

## Construire l’image

Depuis le répertoire contenant `Dockerfile` et `convert.py` :

```bash
docker build -t convert .
```

- `docker build` construit l’image ;
- `-t convert` lui attribue le nom `convert` ;
- `.` indique que le contexte de construction est le répertoire courant.

## Lancer une conversion

```bash
docker run --rm convert 2599
```

L’option `--rm` supprime automatiquement le conteneur lorsqu’il a terminé son exécution. Elle évite l’accumulation de conteneurs arrêtés dans :

```bash
docker ps -a
```

Sans `--rm`, Docker conserve chaque instance et lui attribue automatiquement un nom, par exemple :

```text
pensive_moser
vibrant_hermann
laughing_clarke
```

## Mode interactif

Le programme peut également demander le nombre à convertir :

```bash
docker run -it --rm convert
```

L’option `-it` permet de saisir une valeur dans le terminal.

Sans argument et sans `-it`, aucune entrée interactive n’est disponible dans le conteneur.

## Créer une commande courte

Pour éviter d’écrire à chaque fois :

```bash
docker run --rm convert 2599
```

on peut créer un petit script Bash nommé `convert`.

Créez le fichier :

```bash
nano ~/convert
```

Ajoutez :

```bash
#!/bin/bash

docker run --rm convert "$1"
```

Dans un script Bash, `$1` représente le premier argument placé après le nom du script.

Rendez ensuite le fichier exécutable :

```bash
chmod +x ~/convert
```

Déplacez-le dans un répertoire présent dans la variable `PATH` :

```bash
sudo mv ~/convert /usr/local/bin/convert
```

La conversion peut alors être lancée depuis n’importe quel répertoire :

```bash
convert 2599
```

Le déroulement est le suivant :

```text
convert 2599
    ↓
le script Bash reçoit 2599 dans $1
    ↓
docker run --rm convert 2599
    ↓
ENTRYPOINT ajoute 2599 à python convert.py
    ↓
Python lit 2599 dans sys.argv[1]
```

## Gestion des erreurs

Si l’argument n’est pas un entier :

```bash
convert abc
```

le programme répond :

```text
Erreur : 'abc' n'est pas un entier valide.
```

## Remarque sur les valeurs supérieures à 64 bits

La fonction `choose_width()` retourne 64 bits pour toute valeur dépassant la plage 32 bits. Pour conserver une représentation rigoureuse de type `int64_t`, les valeurs devraient rester comprises entre :

```text
-9 223 372 036 854 775 808
et
 9 223 372 036 854 775 807
```

Au-delà, le masque 64 bits conserve seulement les 64 bits de poids faible.

## Remerciements

La documentation README a été rédigée avec l'aide de ChatGPT par
OpenAI.
