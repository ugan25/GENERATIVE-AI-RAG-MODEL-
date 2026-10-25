import pytest
from calculator import calculate_print_order


def test_expected_example_one():
    assert calculate_print_order(5, 3, "black_white", True, True) == {
        "printed_sides": 15, "paper_sheets": 9, "printing_charge": 30,
        "binding_charge": 90, "total": 120,
    }


def test_expected_example_two():
    assert calculate_print_order(4, 2, "colour", False, False) == {
        "printed_sides": 8, "paper_sheets": 8, "printing_charge": 64,
        "binding_charge": 0, "total": 64,
    }

@pytest.mark.parametrize("pages,copies", [(0, 1), (1, 0), (-1, 2)])
def test_positive_integers_required(pages, copies):
    with pytest.raises(ValueError):
        calculate_print_order(pages, copies, "black_white", False, False)


def test_odd_pages_round_up_per_copy():
    assert calculate_print_order(5, 2, "black_white", True, False)["paper_sheets"] == 6


def test_invalid_colour_mode():
    with pytest.raises(ValueError):
        calculate_print_order(1, 1, "sepia", False, False)
