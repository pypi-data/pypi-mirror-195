r"""
PyByle (Python Bytes File) - A small library for defining and converting encodings

The library currently uses python 3.10 and supports 97 possible encodings
The next version of python 3.11 supports all the same encodings as python 3.10
You can learn more about the list of encodings for different versions
of the interpreter here: https://docs.python.org/3.10/library/codecs.html#standard-encodings

Function list:
 - get_charset(encoding: str) -> str
 - convert_encoding(data: str, *, encoding: str, substitute: str) -> str

 - detect_bytes_encoding(data: bytes) -> str
 - detect_file_encoding(path: str) -> str

Examples:

In  [1]: get_charset('ascii')
Out [2]: ['\x00', '\x01', '\x02', '\x03', '\x04', '\x05', '\x06', '\x07', '\x08', '\t', ...]

In  [1]: convert_encoding('Привет, мир! Hello, world!', encoding='ascii')
Out [2]: ??????, ???! Hello, world!
In  [3]: convert_encoding('Привет, мир! Hello, world!', encoding='ascii', substitute='_')
Out [4]: ______, ___! Hello, world!

In  [1]: detect_bytes_encoding(b'\xd0\x9f\xd1\x80\xd0\xb8\xd0\xb2\xd0\xb5\xd1\x82')
Out [2]: utf-8

In  [1]: detect_file_encoding('example_file.txt')
Out [2]: utf-8
"""


import functools
import os


__all__ = ["get_charset", "convert_encoding", "detect_bytes_encoding", "detect_file_encoding"]


_encodings = ["utf-8", "utf_32_be", "utf_32_le", "utf_16", "utf_16_be", "utf_16_le", "utf_7", "utf_8_sig", "big5",
              "big5hkscs", "cp037", "cp273", "cp424", "cp437", "cp500", "cp720", "cp737", "cp775", "cp850", "cp852",
              "cp855", "cp856", "cp857", "cp858", "cp860", "cp861", "cp862", "cp863", "cp864", "cp865", "cp866",
              "cp869", "cp874", "cp875", "cp932", "cp949", "cp950", "cp1006", "cp1026", "cp1125", "cp1140", "cp1250",
              "cp1251", "cp1252", "cp1253", "cp1254", "cp1255", "cp1256", "cp1257", "cp1258", "euc_jp", "euc_jis_2004",
              "euc_jisx0213", "euc_kr", "gb2312", "gbk", "gb18030", "hz", "iso2022_jp", "iso2022_jp_1", "iso2022_jp_2",
              "iso2022_jp_2004", "iso2022_jp_3", "iso2022_jp_ext", "iso2022_kr", "latin_1", "iso8859_2", "iso8859_3",
              "iso8859_4", "iso8859_5", "iso8859_6", "iso8859_7", "iso8859_8", "iso8859_9", "iso8859_10", "iso8859_11",
              "iso8859_13", "iso8859_14", "iso8859_15", "iso8859_16", "johab", "koi8_r", "koi8_t", "koi8_u", "kz1048",
              "mac_cyrillic", "mac_greek", "mac_iceland", "mac_latin2", "mac_roman", "mac_turkish", "ptcp154",
              "shift_jis", "shift_jis_2004", "shift_jisx0213", "utf_32", "ascii"]


@functools.cache
def get_charset(encoding: str = "ascii") -> list[str]:
    """ Returns a list of valid characters in the given encoding. """

    if encoding not in _encodings:
        raise Exception(f"Failed to find encoding '{encoding}'!")

    output = []
    for character in range(0x110000):
        if letter := chr(character).encode(encoding, errors="ignore"):
            output.append(letter.decode(encoding))

    return output


@functools.cache
def convert_encoding(data: str, *, encoding: str = "ascii", substitute: str = "?") -> str:
    """ Converts a string from one encoding to another, replacing invalid characters. """

    output, supported = "", get_charset(encoding)
    for letter in data:
        output += substitute if letter not in supported else letter

    return output.encode(encoding, errors="ignore").decode(encoding)


@functools.cache
def detect_bytes_encoding(data: bytes) -> str:
    """ The match method tries to pick up an encoding for a byte array. """

    for encoding in _encodings:
        try:
            return (data.decode(encoding), encoding)[1]
        except UnicodeDecodeError:
            continue

    raise Exception("Failed to determine encoding!")


def detect_file_encoding(path: str) -> str:
    """ The selection method tries to select the encoding for the selected file. """

    if os.path.isdir(path):
        raise Exception("The function takes a file, not a directory!")

    if not os.path.exists(path):
        raise Exception("Failed to open the file on the selected path!")

    with open(path, mode="rb") as file:
        bytes_data = file.read()

    return detect_bytes_encoding(bytes_data)
