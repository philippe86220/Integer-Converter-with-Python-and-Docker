
import sys

def choose_width(n):
    if -128 <= n <= 127:
        return 8
    if -32768 <= n <= 32767:
        return 16
    if -2147483648 <= n <= 2147483647:
        return 32
    return 64

def format_binary(n, group_size=4):
    total_bits = choose_width(n)
    mask = (1 << total_bits) - 1
    bits = format(n & mask, f'0{total_bits}b')
    groups = [bits[i:i + group_size] for i in range(0, total_bits, group_size)]
    return ' '.join(groups)


def format_hex(n):
    total_bits = choose_width(n)
    mask = (1 << total_bits) - 1
    hex_digits = total_bits // 4
    hexa = format(n & mask, f'0{hex_digits}X')
    # groupé par octet (2 caractères hex = 1 octet)
    groups = [hexa[i:i + 2] for i in range(0, len(hexa), 2)]
    return ' '.join(groups)


def get_integer():
    # Cas 1 : un argument a été passé en ligne de commande
    if len(sys.argv) > 1:
        try:
            return int(sys.argv[1])
        except ValueError:
            print(f"Erreur : '{sys.argv[1]}' n'est pas un entier valide.")
            sys.exit(1)

    # Cas 2 : mode interactif, on boucle jusqu'à obtenir une saisie valide
    while True:
        try:
            saisie = input("Entrez un entier : ")
            return int(saisie)
        except ValueError:
            print(f"Erreur : '{saisie}' n'est pas un entier valide, réessaie.")
        except EOFError:
            # Pas d'entrée disponible (ex: docker run sans -it)
            print("\nAucune entrée disponible. Utilise 'docker run -it ...' "
                  "pour le mode interactif, ou passe un entier en argument.")
            sys.exit(1)


def main():
    n = get_integer()

    print(f"Décimal     : {n}")
    print(f"Binaire     : {format_binary(n)}")
    print(f"Hexadécimal : 0x{format_hex(n).replace(' ', '')}  ({format_hex(n)})")


if __name__ == "__main__":
    main()
