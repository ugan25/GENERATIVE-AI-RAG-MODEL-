import math

def calculate_print_order(
    pages_per_copy: int,
    copies: int,
    colour_mode: str,
    double_sided: bool,
    binding_required: bool
) -> dict:
    """Calculate quantities and estimated price. This function never prints or uploads files."""
    if isinstance(pages_per_copy, bool) or not isinstance(pages_per_copy, int) or pages_per_copy <= 0:
        raise ValueError("Page count must be a positive integer.")
    if isinstance(copies, bool) or not isinstance(copies, int) or copies <= 0:
        raise ValueError("Number of copies must be a positive integer.")

    colour_mode = str(colour_mode).strip().lower()
    if colour_mode not in {"black_white", "colour"}:
        raise ValueError("Colour mode must be black_white or colour.")

    sides_per_copy = pages_per_copy
    printed_sides = sides_per_copy * copies
    sheets_per_copy = math.ceil(pages_per_copy / 2) if double_sided else pages_per_copy
    paper_sheets = sheets_per_copy * copies

    rate = 2 if colour_mode == "black_white" else 8
    printing_charge = printed_sides * rate
    binding_charge = 30 * copies if binding_required else 0
    total = printing_charge + binding_charge

    return {
        "printed_sides": printed_sides,
        "paper_sheets": paper_sheets,
        "printing_charge": printing_charge,
        "binding_charge": binding_charge,
        "total": total,
        "currency": "INR",
    }
