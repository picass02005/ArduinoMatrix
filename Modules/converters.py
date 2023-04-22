from typing import List


def matrix_to_bytes(matrix_data: List[int]) -> bytes:
    """
    :param matrix_data: 2D matrix with 8 entries of 1 byte long each
    :return: 8 bytes long string
    """

    return bytes(matrix_data)


def int_to_bytes(int_data: int) -> bytes:
    """
    :param int_data: 8 bytes (or less) long int
    :return: 8 bytes long string
    """

    return bytes(reversed([int_data >> i & 255 for i in range(0, 64, 8)]))


def bytes_to_matrix(bytes_data: bytes) -> List[int]:
    """
    :param bytes_data: 8 bytes long string
    :return: 2D matrix with 8 entries of 1 byte long each
    """

    return list(bytes_data)


def bytes_to_int(bytes_data: bytes) -> int:
    """
    :param bytes_data: 8 bytes long string
    :return: 8 bytes (or less) long int
    """

    return sum([bytes_data[i] << (56 - i * 8) for i in range(8)])


def bytes_to_printable(bytes_data: bytes, use_unicode: bool = True) -> str:
    """
    :param bytes_data: 8 bytes long string
    :param use_unicode:
    :return:
    """

    return_str = ""
    for byte in bytes_data:
        for bit in range(7, -1, -1):
            if byte & 1 << bit:
                return_str += "X "

            else:
                return_str += "- "

        return_str += "\n"

    if use_unicode:
        return_str = return_str.replace("X", chr(9899)).replace("-", chr(9898))

    return return_str
