# Line-by-Line Explanation

This section explains how `convert.py` and the `Dockerfile` work.

---

## `convert.py` line by line

### Importing the `sys` module

```python
import sys
```

This line imports Python's standard `sys` module.

The program uses it to access command-line arguments through `sys.argv`.

For example:

```bash
python convert.py -8
```

In this case:

```python
sys.argv[0]  # "convert.py"
sys.argv[1]  # "-8"
```

---

### Selecting the signed width

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

This function selects the smallest signed width able to represent the supplied
value.

The ranges correspond to the usual capacities of signed integers:

| Width | Minimum value | Maximum value |
|---:|---:|---:|
| 8 bits | `-128` | `127` |
| 16 bits | `-32768` | `32767` |
| 32 bits | `-2147483648` | `2147483647` |
| 64 bits | beyond the previous limits | up to the limits supported by the program |

For example:

```text
127   -> 8 bits
128   -> 16 bits
-128  -> 8 bits
-129  -> 16 bits
```

---

### Formatting the binary representation

```python
def format_binary(n, total_bits, group_size=4):
```

This line defines a function that receives:

- `n`: the integer to convert;
- `total_bits`: the selected width, either 8, 16, 32, or 64 bits;
- `group_size`: the number of bits in each group, set to 4 by default.

```python
    mask = (1 << total_bits) - 1
```

This expression builds a mask containing as many `1` bits as the selected width.

For 8 bits:

```text
1 << 8              = 1 0000 0000
(1 << 8) - 1        =   1111 1111
```

The resulting mask is therefore `0xFF`.

For 16 bits, the mask is `0xFFFF`.

```python
    bits = format(n & mask, f"0{total_bits}b")
```

The expression n & mask keeps only the least significant bits of n. The mask clears all higher bits outside the selected width.

For bitwise operations, Python represents negative integers using a two's
complement model with unlimited sign extension.

The mask limits this representation to 8, 16, 32, or 64 bits.

For example, on 8 bits:

```text
 8  -> 0000 1000
-8  -> 1111 1000
```

The `format()` function then converts the value into binary text:

```python
f"0{total_bits}b"
```

This format specification means:

- `b`: produce a binary representation;
- `total_bits`: use the selected width;
- `0`: add leading zeros when necessary.

```python
    groups = [
        bits[i:i + group_size]
        for i in range(0, total_bits, group_size)
    ]
```

This list comprehension splits the binary string into groups of four bits.

For example:

```text
"11111000"
```

becomes:

```python
["1111", "1000"]
```

```python
    return " ".join(groups)
```

The `join()` method combines the groups by inserting a space between them:

```text
1111 1000
```

---

### Formatting the hexadecimal representation

```python
def format_hex(n, total_bits):
```

This function produces the hexadecimal representation of the integer using the
selected width.

```python
    mask = (1 << total_bits) - 1
```

The same mask is built to keep only the bits corresponding to the selected width.

```python
    hex_digits = total_bits // 4
```

One hexadecimal digit represents exactly four bits.

The required number of digits is therefore:

```text
8 bits  -> 2 hexadecimal digits
16 bits -> 4 hexadecimal digits
32 bits -> 8 hexadecimal digits
64 bits -> 16 hexadecimal digits
```

```python
    hexa = format(n & mask, f"0{hex_digits}X")
```

This line:

1. applies the mask with `n & mask`;
2. converts the result to hexadecimal;
3. uses uppercase letters because of `X`;
4. adds leading zeros when necessary.

For example, on 8 bits:

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

The hexadecimal string is split into groups of two characters.

Each group represents one byte.

For example:

```text
1234ABCD
```

becomes:

```text
12 34 AB CD
```

```python
    return " ".join(groups)
```

The groups are joined with spaces to improve readability.

---

### Main function

```python
def main():
```

This function contains the main execution flow of the program.

```python
    if len(sys.argv) > 1:
        n = int(sys.argv[1])
```

`sys.argv` contains the elements supplied on the command line.

If at least one argument was provided, the program reads `sys.argv[1]` and
converts it to an integer with `int()`.

Example:

```bash
python convert.py -8
```

In this case:

```python
n = -8
```

```python
    else:
        n = int(input("Enter an integer: "))
```

If no argument was supplied, the program asks for a value interactively with
`input()`.

```python
    total_bits = choose_width(n)
```

The `choose_width()` function then determines the signed width suitable for the
value.

```python
    binary = format_binary(n, total_bits)
    hexadecimal = format_hex(n, total_bits)
```

These two lines calculate the binary and hexadecimal representations using the
same width.

```python
    print(f"Decimal     : {n}")
```

Displays the original decimal value.

```python
    print(f"Binary      : {binary}")
```

Displays the binary representation grouped into blocks of four bits.

```python
    print(
        f"Hexadecimal : 0x{hexadecimal.replace(' ', '')}"
        f"  ({hexadecimal})"
    )
```

The hexadecimal representation is displayed in two forms:

- a compact form prefixed with `0x`;
- a byte-grouped form in parentheses.

For `-8`, the result on 8 bits is:

```text
Decimal     : -8
Binary      : 1111 1000
Hexadecimal : 0xF8  (F8)
```

The method:

```python
hexadecimal.replace(" ", "")
```

removes the spaces to produce the compact form `0xF8`.

---

### Program entry point

```python
if __name__ == "__main__":
    main()
```

When Python executes the file directly, the special variable `__name__`
contains the value `"__main__"`.

The `main()` function is then called.

However, if `convert.py` is imported from another Python file, `main()` is not
executed automatically.

---

## `Dockerfile` line by line

### Base image

```dockerfile
FROM python:3.12-slim
```

This instruction uses the official Python 3.12 image as the base image.

The `slim` variant contains fewer packages than the standard image, which helps
reduce the size of the final image.

---

### Working directory

```dockerfile
WORKDIR /app
```

This instruction sets `/app` as the working directory inside the container.

Docker automatically creates this directory if it does not already exist.

The following instructions then use this directory as their reference location.

---

### Copying the program

```dockerfile
COPY convert.py .
```

This instruction copies `convert.py` from the build context into the container's
working directory.

Because `WORKDIR` is set to `/app`, the file is copied to:

```text
/app/convert.py
```

The dot `.` therefore refers to the current working directory in the image.

---

### Main command

```dockerfile
ENTRYPOINT ["python", "convert.py"]
```

This instruction defines the main command executed when the container starts.

The JSON form used here is called the *exec form*.

The command:

```bash
docker run --rm convert -8
```

is equivalent to running the following command inside the container:

```bash
python convert.py -8
```

The `-8` argument, placed after the image name, is appended to the command
defined by `ENTRYPOINT`.

It therefore becomes:

```python
sys.argv[1]
```

inside the Python program.

The Docker option `--rm` asks Docker to remove the container automatically when
it stops.

To use the interactive mode of the program, a terminal must be allocated:

```bash
docker run -it --rm convert
```

The options then have the following roles:

- `-i` keeps standard input open;
- `-t` allocates a pseudo-terminal;
- `--rm` removes the container after execution.

---

## Complete execution flow

With the command:

```bash
docker run --rm convert -8
```

Docker performs the following steps:

1. it creates a container from the `convert` image;
2. it executes the command defined by `ENTRYPOINT`;
3. it appends `-8` as an argument;
4. Python therefore runs `python convert.py -8`;
5. `sys.argv[1]` contains `"-8"`;
6. `int()` converts that string into an integer;
7. `choose_width(-8)` selects 8 bits;
8. the `0xFF` mask limits the representation to 8 bits;
9. the program displays:

```text
Decimal     : -8
Binary      : 1111 1000
Hexadecimal : 0xF8  (F8)
```

10. the container stops and is then removed because of `--rm`.
