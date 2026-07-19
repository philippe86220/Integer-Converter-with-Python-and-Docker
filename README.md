# Integer Converter with Python and Docker

This small project converts a decimal integer into its binary and
hexadecimal representations. For negative numbers, it uses two's
complement.

The program automatically selects the smallest signed width suitable for
the value: 8, 16, 32, or 64 bits.

## Examples

``` text
$ convert 127
Decimal     : 127
Binary      : 0111 1111
Hexadecimal : 0x7F  (7F)
```

``` text
$ convert -129
Decimal     : -129
Binary      : 1111 1111 0111 1111
Hexadecimal : 0xFF7F  (FF 7F)
```

## Project Structure

``` text
.
├── convert.py
├── Dockerfile
└── README.md
```

## How the Python Program Works

### Choosing the Width

The `choose_width()` function determines the smallest signed integer
type capable of storing the value:

``` python
def choose_width(n):
    if -128 <= n <= 127:
        return 8
    if -32768 <= n <= 32767:
        return 16
    if -2147483648 <= n <= 2147483647:
        return 32
    return 64
```

These limits correspond to the following C/C++ types:

  ------------------------------------------------------------------------
            Width C/C++ type                Signed range
  --------------- ------------------------- ------------------------------
           8 bits `int8_t`                  -128 to 127

          16 bits `int16_t`                 -32,768 to 32,767

          32 bits `int32_t`                 -2,147,483,648 to
                                            2,147,483,647

          64 bits `int64_t`                 -9,223,372,036,854,775,808 to
                                            9,223,372,036,854,775,807
  ------------------------------------------------------------------------

### Two's Complement

Python integers have arbitrary precision. To obtain a finite two's
complement representation, the program applies a bit mask matching the
selected width:

``` python
mask = (1 << total_bits) - 1
value = n & mask
```

For example, `-128` on 8 bits becomes:

``` text
1000 0000
```

### Binary Output

The binary representation is left-padded with zeros and grouped into
4-bit blocks.

### Hexadecimal Output

The number of hexadecimal digits depends on the selected width. The
output is grouped by bytes (two hexadecimal digits per byte).

## Dockerfile

``` dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY convert.py .

ENTRYPOINT ["python", "convert.py"]
```

`ENTRYPOINT` defines the command executed inside the container. Any
argument placed after the image name is automatically appended to this
command.

For example:

``` bash
docker run --rm convert 15998
```

is equivalent, inside the container, to:

``` bash
python convert.py 15998
```

## Build the Image

``` bash
docker build -t convert .
```

## Run a Conversion

``` bash
docker run --rm convert 2599
```

The `--rm` option automatically removes the container when it exits,
preventing stopped containers from accumulating in:

``` bash
docker ps -a
```

Without `--rm`, Docker keeps each instance and assigns it an
automatically generated name such as:

``` text
pensive_moser
vibrant_hermann
laughing_clarke
```

## Interactive Mode

``` bash
docker run -it --rm convert
```

## Creating a Short Command

Create a small Bash script named `convert`:

``` bash
#!/bin/bash

docker run --rm convert "$1"
```

Make it executable:

``` bash
chmod +x ~/convert
sudo mv ~/convert /usr/local/bin/convert
```

You can then simply run:

``` bash
convert 2599
```

Execution flow:

``` text
convert 2599
    ↓
Bash script receives 2599 in $1
    ↓
docker run --rm convert 2599
    ↓
ENTRYPOINT executes python convert.py 2599
    ↓
Python reads 2599 from sys.argv[1]
```

## Error Handling

``` text
Error: 'abc' is not a valid integer.
```

## Acknowledgements

The README documentation was written with the assistance of ChatGPT by
OpenAI.



