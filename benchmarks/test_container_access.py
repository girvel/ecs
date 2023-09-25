from dataclasses import dataclass


def test_dict(benchmark):
    d = {"value": 43}
    assert benchmark(lambda: d["value"] ** 2) == 43 ** 2

def test_object(benchmark):
    class D:
        value: int

        def __init__(self, value):
            self.value = value

    d = D(43)

    assert benchmark(lambda: d.value ** 2) == 43 ** 2

def test_data_object(benchmark):
    @dataclass
    class D:
        value: int

    d = D(43)

    assert benchmark(lambda: d.value ** 2) == 43 ** 2
