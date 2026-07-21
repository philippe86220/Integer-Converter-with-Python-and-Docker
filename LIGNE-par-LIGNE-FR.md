
# Explication ligne par ligne

Cette section explique le fonctionnement de `convert.py` et du `Dockerfile`.

---

## `convert.py` ligne par ligne

### Importation du module `sys`

```python
import sys
```

Cette ligne importe le module standard `sys`.

Le programme l’utilise pour accéder aux arguments transmis sur la ligne de commande
avec `sys.argv`.

Par exemple :

```bash
python convert.py -8
```

Dans ce cas :

```python
sys.argv[0]  # "convert.py"
sys.argv[1]  # "-8"
```

---

### Sélection de la largeur signée

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

Cette fonction sélectionne la plus petite largeur signée capable de représenter
la valeur reçue.

Les intervalles correspondent aux capacités habituelles des entiers signés :

| Largeur | Valeur minimale | Valeur maximale |
|---:|---:|---:|
| 8 bits | `-128` | `127` |
| 16 bits | `-32768` | `32767` |
| 32 bits | `-2147483648` | `2147483647` |
| 64 bits | au-delà des limites précédentes | jusqu’aux limites prévues par le programme |

Par exemple :

```text
127   -> 8 bits
128   -> 16 bits
-128  -> 8 bits
-129  -> 16 bits
```

---

### Formatage de la représentation binaire

```python
def format_binary(n, total_bits, group_size=4):
```

Cette ligne définit une fonction qui reçoit :

- `n` : l’entier à convertir ;
- `total_bits` : la largeur sélectionnée, soit 8, 16, 32 ou 64 bits ;
- `group_size` : le nombre de bits par groupe, fixé à 4 par défaut.

```python
    mask = (1 << total_bits) - 1
```

Cette expression construit un masque contenant autant de bits `1` que la largeur
sélectionnée.

Pour 8 bits :

```text
1 << 8              = 1 0000 0000
(1 << 8) - 1        =   1111 1111
```

Le masque obtenu vaut donc `0xFF`.

Pour 16 bits, le masque vaut `0xFFFF`.

```python
    bits = format(n & mask, f"0{total_bits}b")
```

L’expression `n & mask` conserve uniquement les bits de poids faible correspondant
à la largeur sélectionnée.

Pour les opérations bit à bit, Python représente les entiers négatifs selon un
modèle en complément à deux avec une extension illimitée du bit de signe.

Le masque limite cette représentation à 8, 16, 32 ou 64 bits.

Par exemple, sur 8 bits :

```text
 8  -> 0000 1000
-8  -> 1111 1000
```

La fonction `format()` convertit ensuite la valeur en texte binaire :

```python
f"0{total_bits}b"
```

Cette spécification signifie :

- `b` : produire une représentation binaire ;
- `total_bits` : utiliser la largeur sélectionnée ;
- `0` : ajouter des zéros à gauche lorsque cela est nécessaire.

```python
    groups = [
        bits[i:i + group_size]
        for i in range(0, total_bits, group_size)
    ]
```

Cette compréhension de liste découpe la chaîne binaire en groupes de quatre bits.

Par exemple :

```text
"11111000"
```

devient :

```python
["1111", "1000"]
```

```python
    return " ".join(groups)
```

La méthode `join()` réunit les groupes en insérant un espace entre eux :

```text
1111 1000
```

---

### Formatage de la représentation hexadécimale

```python
def format_hex(n, total_bits):
```

Cette fonction produit la représentation hexadécimale de l’entier sur la largeur
sélectionnée.

```python
    mask = (1 << total_bits) - 1
```

Le même masque est construit afin de conserver uniquement les bits correspondant
à la largeur sélectionnée.

```python
    hex_digits = total_bits // 4
```

Un chiffre hexadécimal représente exactement quatre bits.

Le nombre de chiffres nécessaires est donc :

```text
8 bits  -> 2 chiffres hexadécimaux
16 bits -> 4 chiffres hexadécimaux
32 bits -> 8 chiffres hexadécimaux
64 bits -> 16 chiffres hexadécimaux
```

```python
    hexa = format(n & mask, f"0{hex_digits}X")
```

Cette ligne :

1. applique le masque avec `n & mask` ;
2. convertit le résultat en hexadécimal ;
3. utilise des lettres majuscules grâce à `X` ;
4. ajoute des zéros à gauche si nécessaire.

Par exemple, sur 8 bits :

```text
 8  -> 08
-8  -> F8
```

```python
    groups = [
        hexa[i:i + 2]
        for i in range(0, len(hexa), 2)
    ]
```

La chaîne hexadécimale est découpée en groupes de deux caractères.

Chaque groupe représente un octet.

Par exemple :

```text
1234ABCD
```

devient :

```text
12 34 AB CD
```

```python
    return " ".join(groups)
```

Les groupes sont réunis avec des espaces pour améliorer la lisibilité.

---

### Fonction principale

```python
def main():
```

Cette fonction contient le déroulement principal du programme.

```python
    if len(sys.argv) > 1:
        n = int(sys.argv[1])
```

`sys.argv` contient les éléments transmis sur la ligne de commande.

Si au moins un argument a été fourni, le programme lit `sys.argv[1]` et le
convertit en entier avec `int()`.

Exemple :

```bash
python convert.py -8
```

Dans ce cas :

```python
n = -8
```

```python
    else:
        n = int(input("Entrez un entier : "))
```

Si aucun argument n’a été fourni, le programme demande une valeur de manière
interactive avec `input()`.

```python
    total_bits = choose_width(n)
```

La fonction `choose_width()` détermine ensuite la largeur signée adaptée à la
valeur.

```python
    binary = format_binary(n, total_bits)
    hexadecimal = format_hex(n, total_bits)
```

Ces deux lignes calculent les représentations binaire et hexadécimale en utilisant
la même largeur.

```python
    print(f"Décimal     : {n}")
```

Affiche la valeur décimale originale.

```python
    print(f"Binaire     : {binary}")
```

Affiche la représentation binaire regroupée par blocs de quatre bits.

```python
    print(
        f"Hexadécimal : 0x{hexadecimal.replace(' ', '')}"
        f"  ({hexadecimal})"
    )
```

La représentation hexadécimale est affichée sous deux formes :

- une forme compacte précédée de `0x` ;
- une forme regroupée par octets entre parenthèses.

Pour `-8`, le résultat sur 8 bits est :

```text
Décimal     : -8
Binaire     : 1111 1000
Hexadécimal : 0xF8  (F8)
```

La méthode :

```python
hexadecimal.replace(" ", "")
```

supprime les espaces afin de produire la forme compacte `0xF8`.

---

### Point d’entrée du programme

```python
if __name__ == "__main__":
    main()
```

Lorsque Python exécute directement le fichier, la variable spéciale `__name__`
contient la valeur `"__main__"`.

La fonction `main()` est alors appelée.

En revanche, si `convert.py` est importé depuis un autre fichier Python, `main()`
n’est pas exécutée automatiquement.

---

## `Dockerfile` ligne par ligne

### Image de base

```dockerfile
FROM python:3.12-slim
```

Cette instruction utilise l’image officielle Python 3.12 comme base.

La variante `slim` contient moins de paquets que l’image standard, ce qui permet
de réduire la taille de l’image finale.

---

### Répertoire de travail

```dockerfile
WORKDIR /app
```

Cette instruction définit `/app` comme répertoire de travail à l’intérieur du
conteneur.

Docker crée automatiquement ce dossier s’il n’existe pas.

Les instructions suivantes utilisent ensuite ce répertoire comme emplacement de
référence.

---

### Copie du programme

```dockerfile
COPY convert.py .
```

Cette instruction copie `convert.py` depuis le contexte de construction vers le
répertoire de travail du conteneur.

Comme `WORKDIR` vaut `/app`, le fichier est copié ici :

```text
/app/convert.py
```

Le point `.` désigne donc le répertoire de travail courant dans l’image.

---

### Commande principale

```dockerfile
ENTRYPOINT ["python", "convert.py"]
```

Cette instruction définit la commande principale exécutée au démarrage du
conteneur.

La forme JSON utilisée ici est appelée forme *exec*.

La commande :

```bash
docker run --rm convert -8
```

revient à exécuter dans le conteneur :

```bash
python convert.py -8
```

L’argument `-8`, placé après le nom de l’image, est ajouté à la commande définie
par `ENTRYPOINT`.

Il devient donc :

```python
sys.argv[1]
```

dans le programme Python.

L’option Docker `--rm` demande la suppression automatique du conteneur lorsqu’il
se termine.

Pour utiliser le mode interactif du programme, il faut allouer un terminal :

```bash
docker run -it --rm convert
```

Les options ont alors les rôles suivants :

- `-i` conserve l’entrée standard ouverte ;
- `-t` alloue un pseudo-terminal ;
- `--rm` supprime le conteneur après son exécution.

---

## Enchaînement complet

Avec la commande :

```bash
docker run --rm convert -8
```

Docker effectue les étapes suivantes :

1. il crée un conteneur à partir de l’image `convert` ;
2. il exécute la commande définie par `ENTRYPOINT` ;
3. il ajoute `-8` comme argument ;
4. Python exécute donc `python convert.py -8` ;
5. `sys.argv[1]` contient `"-8"` ;
6. `int()` convertit cette chaîne en entier ;
7. `choose_width(-8)` sélectionne 8 bits ;
8. le masque `0xFF` limite la représentation à 8 bits ;
9. le programme affiche :

```text
Décimal     : -8
Binaire     : 1111 1000
Hexadécimal : 0xF8  (F8)
```

10. le conteneur s’arrête puis est supprimé grâce à `--rm`.
