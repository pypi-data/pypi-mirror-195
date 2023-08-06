import math
import random

import pytest

from cvectors import Vector, _from_complex


def random_vectors(n=1000):
    for _ in range(n):
        components = []
        for _ in range(2):
            if random.randrange(50):
                components.append(
                    random.uniform(
                        -(2 ** random.randint(-5, 5)), 2 ** random.randrange(-5, 5)
                    )
                )
            else:
                components.append(0)
        yield Vector(*components)


def test_equality():
    assert Vector(1, 2) == Vector(1, 2)
    assert Vector(9, -2) == Vector(9, -2)
    assert Vector(0, 0) == Vector(0, -0)


def test_plus():
    assert Vector(2, 3) + Vector(9, 1) == Vector(11, 4)
    assert Vector(0, -3) + Vector(-3, 1) == Vector(-3, -2)


def test_add_distributes():
    for v1, v2 in zip(random_vectors(), random_vectors()):
        assert v1 + v2 == Vector(v1.x + v2.x, v1.y + v2.y)


def test_minus():
    assert Vector(3, 1) - Vector(2, 6) == Vector(1, -5)
    assert Vector(9, 0) - Vector(20, -1) == Vector(-11, 1)


def test_minus_distributes():
    for v1, v2 in zip(random_vectors(), random_vectors()):
        assert v1 - v2 == Vector(v1.x - v2.x, v1.y - v2.y)


def test_scale():
    assert Vector(9, -1) * 2 == Vector(18, -2)
    assert Vector(5, -6) * 0 == Vector(0, 0)
    assert Vector(-3, 2) * -8 == Vector(24, -16)
    assert isinstance(Vector(9, 0) * 3, Vector)
    assert isinstance(-8 * Vector(3, -2), Vector)


def test_div_scale():
    assert Vector(-8, 10) / 4 == Vector(-2, 2.5)
    assert isinstance(Vector(9, 0) / 10, Vector)
    with pytest.raises(TypeError):
        1 / Vector(3, 2)


def test_from_complex():
    for v in random_vectors():
        assert v == _from_complex(complex(v.x, v.y))
    assert _from_complex(2 + 3j) == Vector(2, 3)
    assert _from_complex(1j) == Vector(0, 1)


def test_from_bad_iterable():
    with pytest.raises(TypeError):
        Vector([1])
    with pytest.raises(TypeError):
        Vector([1, 2])
    with pytest.raises(TypeError):
        Vector([1, 2, 3])


def test_from_random_stuff():
    with pytest.raises(TypeError):

        class Foo:
            pass

        Vector(Foo())
    with pytest.raises(TypeError):
        Vector(lambda x: 0)
    with pytest.raises(TypeError):
        Vector(int)
    with pytest.raises(TypeError):
        Vector("bar")
    with pytest.raises(TypeError):
        Vector(y=3)
    with pytest.raises(TypeError):
        Vector(x="6", y="-3")


def test_repr_():
    assert repr(Vector(5.0, 6.0)) == "Vector(5.0, 6.0)"


def test_str():
    assert str(Vector(-1.0, 1.0)) == "(-1.0 1.0)"


def test_iteration():
    for v in random_vectors():
        for component in v:
            assert component in {v.x, v.y}


def test_properties():
    assert Vector(2, 3).x == 2
    assert Vector(9, -3).y == -3


def test_r():
    assert Vector(3, -4).r == abs(Vector(3, -4)) == 5
    assert Vector(0, 0).r == abs(Vector(0, 0)) == 0
    assert Vector.from_polar(r=-1, theta=2).r == 1

    for v in random_vectors():
        assert v.r == abs(v)


def test_theta():
    assert Vector(1, 1).theta == math.pi / 4
    assert Vector(0, -1).theta == -math.pi / 2
    assert Vector(-1, -1).theta == -3 * math.pi / 4
    assert Vector.from_polar(r=2, theta=1).theta == 1


def test_polar_creation():
    assert Vector.from_polar(r=2, theta=0) == Vector(2, 0)
    assert Vector.from_polar(3, math.pi).rec() == pytest.approx(Vector(-3, 0).rec())
    assert Vector.from_polar(theta=0, r=-1) == Vector(-1, 0)
    assert Vector.from_polar(r=0, theta=501).r == 0


def test_getitem():
    vec = Vector(3, -9)
    assert vec[0] == vec[-2] == 3
    assert vec[1] == vec[-1] == -9
    with pytest.raises(IndexError):
        vec[3]
        vec[-3]


def test_dot():
    assert Vector(-1, 2).dot(Vector(1, 4)) == 7
    assert Vector(0, -2).dot(Vector(9, -1)) == 2


def test_perp_dot():
    assert Vector(-1, 1).perp_dot(Vector(1, 1)) == -2
    assert Vector(0, 1).perp_dot(Vector(0, 1)) == 0


def test_perp():
    assert Vector(3, 1).perp() == Vector(-1, 3)
    assert Vector(-2, 4).perp() == Vector(-4, -2)


def test_round():
    assert Vector(2.3, 1.9).round() == (2, 2)
    assert Vector(1.49, -0.2).round() == (1, 0)
    for i in range(2):
        assert isinstance(Vector(-12.1, 15).round(0)[i], float)
        assert isinstance(Vector(-12.1, 15).round()[i], int)
    assert Vector(5.1209, -3.3211).round(1) == (5.1, -3.3)
    assert Vector(5.1209, -3.3211).round(1) == (5.1, -3.3)


def test_rotate():
    assert Vector(2, 3).rotate(math.pi).rec() == pytest.approx(Vector(-2, -3).rec())
    assert Vector(2, 3).rotate(math.pi / 2).rec() == pytest.approx(Vector(-3, 2).rec())
    assert Vector(2, 3).rotate(math.tau).rec() == pytest.approx(Vector(2, 3).rec())


def test_unary_minus():
    assert -Vector(-2, 0) == Vector(2, 0)


def test_from_object():
    class Foo:
        def __init__(self, x, y):
            self.x = x
            self.y = y

    with pytest.raises(TypeError):
        Vector(Foo(4, 9))


def test_rec():
    for _ in range(1000):
        x = random.uniform(-999, 999)
        y = random.uniform(-999, 999)
        assert Vector(x, y).rec() == (x, y)


def test_pol():
    for _ in range(1000):
        r = random.uniform(0, 999)
        theta = random.uniform(-math.pi, math.pi)
        pol = Vector.from_polar(r, theta).pol()
        assert math.isclose(r, pol[0])
        assert math.isclose(theta, pol[1])


def test_hat():
    assert Vector(-3, 4).hat() == Vector(-3 / 5, 4 / 5)
    for _ in range(1000):
        vec = Vector.from_polar(r=1, theta=random.uniform(-999, 999)).hat()
        assert vec.hat() == vec


def test_neg():
    for _ in range(1000):
        x = random.uniform(-999, 999)
        y = random.uniform(-999, 999)
        assert -Vector(x, y) == Vector(-x, -y)


def test_reversed():
    for _ in range(1000):
        vec = Vector(random.uniform(-999, 999), random.uniform(-999, 999))
        assert list(reversed(vec)) == list(reversed(list(vec)))


def test_contains():
    for _ in range(1000):
        vec = Vector(random.uniform(-999, 999), random.uniform(-999, 999))
        assert vec.x in vec
        assert vec.y in vec
        assert abs(vec.x) + abs(vec.y) + 1 not in vec


def test_index():
    for _ in range(1000):
        vec = Vector(random.uniform(-999, 999), random.uniform(-999, 999))
        assert vec.index(vec.x) == 0
        assert vec.index(vec.y, 1) == 1
        if vec.x != vec.y:
            assert vec.index(vec.y) == 1
        with pytest.raises(ValueError):
            vec.index(None)


def test_count():
    for _ in range(1000):
        vec = Vector(random.uniform(-999, 999), random.uniform(-999, 999))
        if vec.x != vec.y:
            assert vec.count(vec.x) == 1
            assert vec.count(vec.y) == 1
        assert vec.count(None) == 0
