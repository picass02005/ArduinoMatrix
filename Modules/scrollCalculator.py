from typing import List

from Modules.converters import matrix_to_bytes


def calcul_scroll_rtl(extended_matrix: List[int], blank_in: bool = False, blank_out: bool = False) -> List[bytes]:
    """
    :param extended_matrix:
    :param blank_in:  Set it to False if you want an in slide at the beginning
    :param blank_out: Set it to True if you want an out slide at the end
    :return: A list containing all frames as byte format
    """

    matrix_size = max([i.bit_length() for i in extended_matrix])

    if matrix_size < 8:
        matrix_size = 8

    if blank_in:
        offset_in = 8

    else:
        offset_in = 0

    frames = [matrix_to_bytes([extended_matrix[i] >> (matrix_size + offset_in - 8) for i in range(8)])]

    if blank_out:
        extended_matrix = [extended_matrix[i] << 8 for i in range(8)]
        offset_out = -1
    else:
        extended_matrix = [(extended_matrix[i] << 8) + (extended_matrix[i] >> (matrix_size - 8)) for i in range(8)]
        offset_out = 7

    if not (blank_in or blank_out):
        offset_out = 0

    for i in range(matrix_size + offset_in - 1, offset_out, -1):
        frame = [(i & 0x7f) << 1 for i in bytearray(frames[-1])]

        for bit in range(8):
            if (extended_matrix[bit] & (1 << i)).bit_count():
                frame[bit] += 1

        frames.append(bytes(frame))

    return frames
