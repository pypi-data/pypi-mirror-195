"""A package for using complex numbers as 2D vectors."""
from __future__ import annotations

from cmath import phase, polar, rect
from collections.abc import Iterator, Sequence
from typing import Literal, NoReturn, overload

__all__ = ["Vector"]


_object_setattr = object.__setattr__


class Vector(Sequence[float]):
    """A two-dimensional vector."""

    __slots__ = ("_complex",)
    _complex: complex

    def __init__(self, /, x: float, y: float) -> None:
        """Create a Vector from a single argument or x, y pair."""
        _object_setattr(self, "_complex", complex(x, y))

    def __eq__(self, other: object, /) -> bool:
        if isinstance(other, Vector):
            return self._complex == other._complex
        return NotImplemented

    def __hash__(self, /) -> int:
        return hash(self._complex)

    def __setattr__(self, name: str, value: object, /) -> NoReturn:
        raise AttributeError("Vectors are immutable")

    def __delattr__(self, name: str, /) -> NoReturn:
        raise AttributeError("Vectors are immutable")

    @classmethod
    def from_polar(cls, r: float, theta: float) -> Vector:
        """Create a Vector from polar coordinates."""
        return _from_complex(rect(r, theta))

    def dot(self, other: Vector, /) -> float:
        """Return the dot product of self and other."""
        return (
            self._complex.real * other._complex.real
            + self._complex.imag * other._complex.imag
        )

    def perp_dot(self, other: Vector, /) -> float:
        """
        Return the perp dot product of self and other.

        This is the signed area of the parallelogram they define. It is
        also one of the 'cross products' that can be defined on 2D
        vectors.
        """
        return (
            self._complex.real * other._complex.imag
            - self._complex.imag * other._complex.real
        )

    def perp(self, /) -> Vector:
        """
        Return the Vector, rotated anticlockwise by pi / 2.

        This is one of the 'cross products' that can be defined on 2D
        vectors. Use -Vector.perp() for a clockwise rotation.
        """
        return _from_complex(self._complex * 1j)

    def rotate(self, /, angle: float) -> Vector:
        """
        Return a self, rotated by angle anticlockwise.

        Use negative angles for a clockwise rotation.
        """
        return _from_complex(self._complex * rect(1, angle))

    def hat(self, /) -> Vector:
        """Return a Vector with the same direction, but unit length."""
        return _from_complex(self._complex / abs(self._complex))

    def rec(self, /) -> tuple[float, float]:
        """Get the vector as (x, y)."""
        return (self._complex.real, self._complex.imag)

    def pol(self, /) -> tuple[float, float]:
        """Get the vector as (r, theta)."""
        return polar(self._complex)

    @overload
    def round(self, /, ndigits: None = ...) -> tuple[int, int]:
        ...

    @overload
    def round(self, /, ndigits: int) -> tuple[float, float]:
        ...

    def round(self, /, ndigits=None):
        """Get the vector with both components rounded, as a tuple."""
        return (round(self._complex.real, ndigits), round(self._complex.imag, ndigits))

    def __str__(self, /) -> str:
        return f"({self._complex.real} {self._complex.imag})"

    def __repr__(self, /) -> str:
        return (
            f"{self.__class__.__qualname__}({self._complex.real}, {self._complex.imag})"
        )

    def __len__(self, /) -> Literal[2]:
        return 2

    @overload
    def __getitem__(self, key: int, /) -> float:
        ...

    @overload
    def __getitem__(self, key: slice, /) -> tuple[float, ...]:
        ...

    def __getitem__(self, key, /):
        return (self._complex.real, self._complex.imag)[key]

    def __iter__(self, /) -> Iterator[float]:
        yield self._complex.real
        yield self._complex.imag

    def __reversed__(self, /) -> Iterator[float]:
        yield self._complex.imag
        yield self._complex.real

    def __contains__(self, item: object, /) -> bool:
        return item == self._complex.real or item == self._complex.imag

    def index(self, value: object, start: int = 0, stop: int = 2, /) -> int:
        return (self._complex.real, self._complex.imag).index(value, start, stop)

    def count(self, value: object, /) -> int:
        return (self._complex.real, self._complex.imag).count(value)

    def __neg__(self, /) -> Vector:
        return _from_complex(-self._complex)

    def __add__(self, other: Vector, /) -> Vector:
        return _from_complex(self._complex + other._complex)

    def __sub__(self, other: Vector, /) -> Vector:
        return _from_complex(self._complex - other._complex)

    def __mul__(self, value: float, /) -> Vector:
        return _from_complex(self._complex * value)

    def __truediv__(self, value: float, /) -> Vector:
        return _from_complex(self._complex / value)

    __rmul__ = __mul__

    def __abs__(self, /) -> float:
        return abs(self._complex)

    def __copy__(self, /) -> Vector:
        return self

    def __deepcopy__(self, _, /) -> Vector:
        return self

    @property
    def x(self) -> float:
        """The horizontal component of the vector."""
        return self._complex.real

    @property
    def y(self) -> float:
        """The vertical component of the vector."""
        return self._complex.imag

    @property
    def r(self) -> float:
        """The radius of the vector."""
        return abs(self._complex)

    @property
    def theta(self) -> float:
        """
        The angle of the vector, anticlockwise from the horizontal.

        Negative values are clockwise. Returns values in the range
        [-pi, pi]. See documentation of cmath.phase for details.
        """
        return phase(self._complex)


def _from_complex(
    z, _object_setattr=object.__setattr__, _vector=Vector, _vector_new=Vector.__new__, /
):
    _object_setattr(new := _vector_new(_vector), "_complex", z)
    return new
