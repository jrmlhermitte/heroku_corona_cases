from corona_stats.data.numerical_range import NumericalRange


def test_in_bounds_without_endpoint():
    range = NumericalRange(start=0, end=1, include_endpoint=False)
    assert not range.within_bounds(-1)
    assert range.within_bounds(0)
    assert range.within_bounds(0.1)
    assert range.within_bounds(0.9)
    assert not range.within_bounds(1)


def test_in_bounds_with_endpoint():
    range = NumericalRange(start=0, end=1, include_endpoint=True)
    assert range.within_bounds(0)
    assert range.within_bounds(0.1)
    assert range.within_bounds(0.9)
    assert range.within_bounds(1)
    assert not range.within_bounds(2)
