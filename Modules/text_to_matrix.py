import json
from typing import Union, List

from Modules.converters import int_to_bytes, bytes_to_matrix
from Modules.logs import Logs


class Font:
    def __init__(self):
        self.font_cache = {}

        self.cache_font()

    def char_to_font(self, character: str, font: Union[None, dict] = None) -> bytes:
        """
        :param character: Character we want to get from cached font
        :param font: The font you want to use, set it to None to use cached font
        :return: Bytes representing character
        """

        if font is None:
            used_font = self.font_cache

        else:
            used_font = font

        if character not in used_font:
            character = "UNKNOWN"

        return int_to_bytes(int(used_font[character], 16))

    def cache_font(self) -> None:
        """
        :return: Reload font cache from font.json
        """

        with open("Modules/font.json", "r") as f:
            font = json.loads(f.read())

        if not self.__check_font(font):
            Logs.error("Current font invalid, can't cache it")
            return

        self.font_cache = font
        Logs.info("Current font cached")

    def text_to_matrix(self, text: str, font: Union[None, dict] = None) -> List[int]:
        """
        :param text: Text you want to convert into an extended matrix
        :param font: Font you want to use, set to None to use cached font
        :return: Extended matrix created
        """

        extended_matrix = [0 for _ in range(8)]

        if font is None:
            used_font = self.font_cache

        else:
            if self.__check_font(font):
                used_font = font

            else:
                Logs.error("Invalid font")

                return extended_matrix

        if self.__is_font_uppercase_only(used_font):
            used_font = self.__make_font_uppercase_only(used_font)
            text = text.upper()

        char_size = used_font["charSize"]

        for i in text:
            char_matrix = self.char_to_font(i, used_font)

            for row in range(8):
                extended_matrix[row] <<= char_size
                extended_matrix[row] += char_matrix[row]

        return extended_matrix

    def __check_font(self, font: dict) -> bool:
        """
        :param font: The font you want to test
        :return: A bool indicating if the font is valid or not
        """

        valid = True

        for i in ["charSize", "UNKNOWN"]:
            if i not in font.keys():
                Logs.error(f"Key {i} not present in this font")
                valid = False

        char_size = font['charSize']

        for key, value in font.items():
            if key != "charSize":
                if key != "UNKNOWN" and len(key) != 1:
                    Logs.error(f"Char {key} is invalid: key isn't 1 char long")
                    valid = False

                for i in bytes_to_matrix(self.char_to_font(key, font)):
                    if i.bit_length() > char_size:
                        Logs.error(f"Char {key} is too long: should be {char_size} long but is {i.bit_length()} long")
                        valid = False

        return valid

    @staticmethod
    def __is_font_uppercase_only(font: dict) -> bool:
        """
        :param font: The font to check
        :return: True if this font is uppercase only
        """

        keys = [i for i in font.keys() if i != "charSize"]

        if keys != [i.upper() for i in keys]:
            return False

        return True

    @staticmethod
    def __make_font_uppercase_only(font: dict) -> dict:
        """
        :param font: The font to use
        :return: Same font but uppercase only
        """

        new_font = {'charSize': font['charSize']}
        old_keys = [i for i in font.keys() if i != "charSize"]

        for i in old_keys:
            if i.upper() in old_keys:
                new_font.update({i: font[i]})

            else:
                new_font.update({i.upper(): font[i]})

        return new_font
