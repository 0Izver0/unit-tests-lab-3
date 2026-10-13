import pytest

from delivery import delivery_cost


# --- happy path -----------------------------------------------------------

def test_one_kg_same_city_gets_twenty_percent_off_base():
    weight, same_city = 1, True
    result = delivery_cost(weight, same_city)
    assert result == 32


def test_two_and_half_kg_other_city_adds_one_full_kg():
    weight, same_city = 2.5, False
    result = delivery_cost(weight, same_city)
    assert result == 55


# --- failure --------------------------------------------------------------

def test_zero_weight_is_rejected():
    with pytest.raises(ValueError, match="positive"):
        delivery_cost(0, True)


def test_negative_weight_is_rejected():
    with pytest.raises(ValueError, match="positive"):
        delivery_cost(-3, False)


@pytest.mark.parametrize("bad_weight", [float("nan"), float("inf")])
def test_non_finite_weight_is_rejected(bad_weight):
    with pytest.raises(ValueError, match="positive"):
        delivery_cost(bad_weight, False)


@pytest.mark.parametrize("bad_weight", ["2", None, True])
def test_non_numeric_weight_is_rejected(bad_weight):
    with pytest.raises(ValueError, match="number"):
        delivery_cost(bad_weight, False)


def test_non_bool_same_city_is_rejected():
    with pytest.raises(ValueError, match="bool"):
        delivery_cost(2, "yes")


# --- boundaries -----------------------------------------------------------

def test_exactly_one_kg_has_no_per_kg_surcharge():
    assert delivery_cost(1, False) == 40


def test_just_under_two_kg_still_has_no_surcharge():
    assert delivery_cost(1.99, False) == 40


def test_exactly_two_kg_adds_first_full_kg():
    assert delivery_cost(2, False) == 55


def test_weight_below_one_kg_pays_base_only():
    assert delivery_cost(0.3, False) == 40


# --- other meaningful cases -----------------------------------------------

def test_same_city_discount_applies_to_total_including_surcharge():
    assert delivery_cost(5, True) == 80


def test_same_city_discount_is_not_applied_to_other_city():
    assert delivery_cost(5, False) == 100


def test_result_is_integer():
    result = delivery_cost(2.5, True)
    assert result == 44
    assert isinstance(result, int)
