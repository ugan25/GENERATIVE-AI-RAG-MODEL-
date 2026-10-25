"""Deterministic print-order calculator; prices are in INR."""
from math import ceil


def calculate_print_order(
    pages_per_copy: int,
    copies: int,
    colour_mode: str,
    double_sided: bool,
    binding_required: bool,
) -> dict:
    if isinstance(pages_per_copy, bool) or not isinstance(pages_per_copy, int) or pages_per_copy <= 0:
        raise ValueError("Page count must be a positive integer.")
    if isinstance(copies, bool) or not isinstance(copies, int) or copies <= 0:
        raise ValueError("Number of copies must be a positive integer.")
    mode = colour_mode.strip().lower().replace("-", "_").replace(" ", "_")
    if mode not in {"black_white", "colour"}:
        raise ValueError("Colour mode must be 'black_white' or 'colour'.")
    if not isinstance(double_sided, bool) or not isinstance(binding_required, bool):
        raise ValueError("Double-sided and binding selections must be boolean values.")

    printed_sides = pages_per_copy * copies
    rate = 2 if mode == "black_white" else 8
    sheets_per_copy = ceil(pages_per_copy / 2) if double_sided else pages_per_copy
    paper_sheets = sheets_per_copy * copies
    printing_charge = printed_sides * rate
    binding_charge = 30 * copies if binding_required else 0
    return {
        "printed_sides": printed_sides,
        "paper_sheets": paper_sheets,
        "printing_charge": printing_charge,
        "binding_charge": binding_charge,
        "total": printing_charge + binding_charge,
    }
