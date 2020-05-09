from corona_stats.data.numerical_range import NumericalRange


def test_in_bounds_without_endpoint():
    numerical_range = NumericalRange(start=0, end=1, include_endpoint=False)
    assert not numerical_range.within_bounds(-1)
    assert numerical_range.within_bounds(0)
    assert numerical_range.within_bounds(0.1)
    assert numerical_range.within_bounds(0.9)
    assert not numerical_range.within_bounds(1)


def test_in_bounds_with_endpoint():
    numerical_range: test_in_bounds_with_endpoint() = NumericalRange(
        start=0, end=1, include_endpoint=True
    )
    assert numerical_range.within_bounds(0)
    assert numerical_range.within_bounds(0.1)
    assert numerical_range.within_bounds(0.9)
    assert numerical_range.within_bounds(1)
    assert not numerical_range.within_bounds(2)
