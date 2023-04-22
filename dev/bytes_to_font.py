from Modules.converters import bytes_to_int


def bytes_to_font(byte_string: bytes) -> str:
    return str(hex(bytes_to_int(byte_string)))[2:]


if __name__ == "__main__":
    from Modules.converters import bytes_to_printable, matrix_to_bytes
    import json

    """
    char_bytes = matrix_to_bytes([
        0b00000,
        0b00000,
        0b00000,
        0b00000,
        0b00000,
        0b00000,
        0b00000,
        0b00000
    ])
    """

    char_bytes = matrix_to_bytes([
        0b01110,
        0b10001,
        0b10001,
        0b10101,
        0b10001,
        0b10001,
        0b10001,
        0b01110
    ])

    print(bytes_to_printable(char_bytes))
    font = bytes_to_font(char_bytes)
    print(font)

    with open("Modules/font.json", "r") as f:
        data = json.loads(f.read())

    while (char := input("Give this char in text\n>>> ")) in data.keys() or len(char) != 1:
        print("This char is already in use or isn't 1 byte length")

    data.update({char: font})

    with open("Modules/font.json", "w") as f:
        f.write(json.dumps(data, indent=4) + "\n")
