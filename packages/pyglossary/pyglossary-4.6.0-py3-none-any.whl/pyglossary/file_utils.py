from itertools import (
	repeat,
	takewhile,
)
from typing import AnyStr


def toBytes(s: "AnyStr") -> bytes:
	return bytes(s, "utf-8") if isinstance(s, str) else bytes(s)


def fileCountLines(filename: str, newline: str = "\n") -> int:
	newline = toBytes(newline)  # required? FIXME
	with open(filename, "rb") as _file:
		bufgen = takewhile(
			lambda x: x, (_file.read(1024 * 1024) for _ in repeat(None)),
		)
		return sum(
			buf.count(newline) for buf in bufgen if buf
		)
