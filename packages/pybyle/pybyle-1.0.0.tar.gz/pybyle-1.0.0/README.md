## PyByle

PyByle is a small library for easy interaction with file and string encodings.

The library currently uses python 3.10 and supports 97 possible encodings
The next version of python 3.11 supports all the same encodings as python 3.10
You can learn more about the list of encodings for different versions
of the interpreter here: https://docs.python.org/3.10/library/codecs.html#standard-encodings

Installing
```bash
pip install pybyle
```

Getting a complete list of supported characters in a given encoding.
```python
import pybyle


pybyle.get_charset('ascii')  # ['\x00', '\x01', '\x02', '\x03', '\x04', ...]
```

Converting a string from one encoding to another. Attention! All unsupported characters will be replaced with the set character!
```python
import pybyle


pybyle.convert_encoding('Привет, мир! Hello, world!', encoding='ascii')  # ??????, ???! Hello, world!
pybyle.convert_encoding('Привет, мир! Hello, world!', encoding='ascii', substitute='_')  # ______, ___! Hello, world!
```

Specifies the encoding of the binary string.
```python
import pybyle


pybyle.detect_bytes_encoding(b'\xd0\x9f\xd1\x80\xd0\xb8\xd0\xb2\xd0\xb5\xd1\x82')  # utf-8
```

Determining the encoding for a given file.
```python
import pybyle


pybyle.detect_file_encoding('example_utf_8_file.txt')  # utf-8
pybyle.detect_file_encoding('example_cp037_file.txt')  # cp037
```