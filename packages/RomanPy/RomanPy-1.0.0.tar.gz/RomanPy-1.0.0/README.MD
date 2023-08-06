# RomanPy

`RomanPy` is a Python library that provides a simple and efficient way to 
convert decimal numbers to Roman numerals. With its user-friendly interface, 
you can easily integrate this library into your Python projects and take 
advantage of its features to convert numerals in a matter of seconds.

## Installation

To install `RomanPy`, you can use pip:

```shell
pip install RomanPy
```

This library has no dependencies and is compatible with Python 3.

## Usage

To use RomanPy, you need to import the `roman` function:

```python
from roman import roman
```

Then, you can convert decimal numbers to Roman numerals:

```python
print(roman(207)) # CCVII
```

ASCII and unicode variants of the Roman numerals are supported in both lower-
and uppercase, using the conventional API known from `str`:

```python
numeral = roman(1776)

numeral = numeral.encode("ascii") # default
numeral = numeral.upper() # default

print(numeral) # MDCCLXXVI (default)

numeral = numeral.lower()

print(numeral) # mdcclxxvi

numeral = numeral.encode("unicode")
numeral = numeral.upper()

print(numeral) # ⅯⅮⅭⅭⅬⅩⅩⅥ

numeral = numeral.lower()

print(numeral) # ⅿⅾⅽⅽⅼⅹⅹⅵ
```

`RomanPy` also allows you to do simple arithmatic with roman numerals:

```python
print(roman(100) + roman(60)) # CLX
print(roman(45) - roman(7)) # XXXIX
print(roman(533) * roman(2)) # MLXVI
print(roman(2460) / roman(10)) # CCXLVI
```

One hand of these operations is also allowed to be an integer:

```python
print(100 + roman(60)) # CLX
print(roman(45) - 7) # XXXIX
print(roman(533) * 2) # MLXVI
print(2460 / roman(10)) # CCXLVI
```

Equality can be determined for other Roman numerals, integers and strings:

```python
print(roman(335) == roman(335)) # True
print(roman(24) == 24) # True
print(roman(1954) == "MCMLIV") # True
```

## Contributing

If you find any bugs or issues with `RomanPy`, please feel free to submit an 
issue on our GitLab page. We welcome any contributions or suggestions to 
improve this library.

## License

`RomanPy` is released under the GPLv3 license. See [LICENSE](LICENCE) for
details.

