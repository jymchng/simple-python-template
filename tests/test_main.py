from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

import pandas as pd
import pytest

from simple_python_template import NewType

if TYPE_CHECKING:
    from typing import Type


class NRIC(NewType(str)):
    country: "str" = "SG"

    def __init__(self, val: "str", hello):
        self.__newtype__(val)
        self._prefix = val[0]
        self._suffix = val[-1]
        self._digits = val[1:-1]
        self.hello = hello

    def __str__(self):
        return f"NRIC(Prefix:{self._prefix}, Suffix:{self._suffix}, Digits:{self._digits})"

    @classmethod
    def __newtype__(cls, nric: "str"):
        alpha_ST = ("J", "Z", "I", "H", "G", "F", "E", "D", "C", "B", "A")
        alpha_GF = ("X", "W", "U", "T", "R", "Q", "P", "N", "M", "L", "K")
        alpha_M = ("K", "L", "J", "N", "P", "Q", "R", "T", "U", "W", "X")
        assert len(str(nric)) == 9, f"NRIC length must be 9, it is `{len(nric)}`"
        assert nric[0] in [
            "S",
            "T",
            "G",
            "F",
            "M",
        ], f"NRIC Prefix must be in ['S', 'T', 'G', 'F'], it is `{nric[0]}`"
        weights = [2, 7, 6, 5, 4, 3, 2]
        digits = nric[1:-1]
        weighted_sum = sum(int(digits[i]) * weights[i] for i in range(7))
        offset = 0
        if nric[0] in ["T", "G"]:
            offset = 4
        if nric[0] == "M":
            offset = 3
        expected_checksum = (offset + weighted_sum) % 11
        if nric[0] in ["S", "T"]:
            assert alpha_ST[expected_checksum] == nric[8], "Checksum is not right"
        elif nric[0] == "M":
            expected_checksum = 10 - expected_checksum
            assert alpha_M[expected_checksum] == nric[8]
        else:
            assert alpha_GF[expected_checksum] == nric[8]


def test_nric():
    nric_one = NRIC("S1234567D", 69)
    assert str(nric_one) == "NRIC(Prefix:S, Suffix:D, Digits:1234567)"
    NRIC("M5398242L", 23)
    NRIC("F5611427X", 57)
    assert nric_one.hello == 69
    nric_one.hello = "bye"
    assert nric_one.hello == "bye"
    assert nric_one._prefix == "S"
    assert nric_one._digits == "1234567"
    assert nric_one._suffix == "D"
    assert type(nric_one).__name__ == NRIC.__name__

    with pytest.raises(Exception):  # noqa: B017
        nric_one = nric_one.replace("S", "Q")

    with pytest.raises(Exception):  # noqa: B017
        nric_one = nric_one + "1234567"


class GoodManNRIC(NRIC):
    def __init__(self, val: "str", hello: "int", bye: "int"):
        super().__init__(val, hello)
        self.bye = bye

    @property
    def prefix(self):
        return self._prefix


def test_goodmannric():
    nric_one = GoodManNRIC("S1234567D", 69, 96)
    GoodManNRIC("M5398242L", 23, 69)
    GoodManNRIC("F5611427X", 57, 69)
    assert nric_one.hello == 69
    assert nric_one.bye == 96
    nric_one.hello = "bye"
    assert nric_one.hello == "bye"
    assert nric_one.prefix == "S"
    assert nric_one._prefix == "S"
    assert nric_one._digits == "1234567"
    assert nric_one._suffix == "D"
    assert type(nric_one).__name__ == GoodManNRIC.__name__

    with pytest.raises(Exception):  # noqa: B017
        nric_one = nric_one.replace("S", "Q")

    with pytest.raises(Exception):  # noqa: B017
        nric_one = nric_one + "1234567"


class BlockchainAddress(NewType(str), ABC):
    is_blockchain_address = True

    @classmethod
    @abstractmethod
    def __newtype__(cls, val: "str") -> "Type[BlockchainAddress]":
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def _validate_address(val: " str") -> "bool":
        raise NotImplementedError

    @classmethod
    def __get_validators__(cls):
        yield cls.__newtype__


class EthereumAddress(BlockchainAddress):
    @classmethod
    def __newtype__(cls, val: "str"):
        assert cls._validate_address(val), f"val = {val} does not match the regex of `Address`"

    def __init__(self, val: "str", is_checksum: "bool"):
        super().__init__(val)
        self.__newtype__(val)
        self._is_checksum = is_checksum

    @property
    def is_checksum(self):
        return self._is_checksum

    @staticmethod
    def _validate_address(address):
        import re

        # Ethereum addresses are 40 hexadecimal characters prefixed with '0x'
        if not re.match(r"^0x[0-9a-fA-F]{40}$", address):
            return False
        return True


def test_ethereum_address():
    expected = "0x4838B106FCe9647Bdf1E7877BF73cE8B0BAD5f97"
    eth_addr = EthereumAddress("0x4838B106FCe9647Bdf1E7877BF73cE8B0BAD5f97", True)
    assert eth_addr == expected
    assert eth_addr.capitalize() == expected.capitalize()
    assert eth_addr.is_checksum
    assert eth_addr.is_blockchain_address


class PositiveInt(NewType(int)):
    is_positive = True

    def __init__(self, val: "int", **kwargs):
        self.__newtype__(val)

        for k, v in kwargs.items():
            setattr(self, k, v)

    @classmethod
    def __newtype__(cls, positive_int: int):
        assert (
            positive_int > 0
        ), f"`PositiveInt` object must be positive, but the passed in value is {positive_int}"
        return positive_int

    @classmethod
    def __get_validators__(cls):
        yield cls.__newtype__


def test_positive_int():
    five = PositiveInt(5, hello=3, bye=2, hey=1, you=29)
    assert five == 5
    assert five.you == 29
    assert five.hey == 1
    assert five.bye == 2
    assert five.hello == 3

    five += 20

    assert five == 25
    assert five.you == 29
    assert five.hey == 1
    assert five.bye == 2
    assert five.hello == 3


class BoundedPositiveInt(PositiveInt):
    def __init__(self, val: "int", upper: "int", lower: "int", *args, **kwargs):
        super().__init__(val, **kwargs)
        self.args = args
        self.upper = upper
        self.lower = lower
        assert self.lower < self < self.upper

    def middle(self):
        return (self.upper + self.lower) / 2


def test_bounded_positive_int():
    ten = BoundedPositiveInt(10, 20, 2, 1, 2, 3, hello=3, bye=4)

    assert ten == 10
    assert ten.upper == 20
    assert ten.lower == 2
    assert ten.args == (1, 2, 3)
    assert ten.middle() == 11

    with pytest.raises(Exception):
        ten += 20

    with pytest.raises(Exception):
        ten -= 30

    assert ten == 10
    ten += 5

    assert ten == 15
    assert ten.upper == 20
    assert ten.lower == 2
    assert ten.args == (1, 2, 3)
    assert ten.middle() == 11

    ten -= 9
    assert ten == 6
    assert ten.upper == 20
    assert ten.lower == 2
    assert ten.middle() == 11
    assert ten.args == (1, 2, 3)


class MyDataFrame(NewType(pd.DataFrame)):
    def __init__(self, df: pd.DataFrame, a, b, c):
        super().__init__(df)
        self.a = a
        self.b = b
        self.c = c

        assert df.shape == (2, 2)


def test_my_dataframe():
    df = pd.DataFrame({"A": [1, 2], "B": [4, 5]})
    my_df = MyDataFrame(df, 1, 2, 3)

    assert my_df.a == 1
    assert my_df.b == 2
    assert my_df.c == 3

    my_df = my_df.T
    print("my_df", my_df, type(my_df))

    assert my_df.a == 1
    assert my_df.b == 2
    assert my_df.c == 3

    assert my_df.at["A", 0] == 1
    assert my_df.at["A", 1] == 2
    assert my_df.at["B", 0] == 4
    assert my_df.at["B", 1] == 5

    my_df.at["A", 1] = 69
    assert my_df.at["A", 1] == 69

    my_df = my_df.T
    with pytest.raises(AssertionError):
        my_df.drop("A", axis=1)

    assert type(my_df) is MyDataFrame
