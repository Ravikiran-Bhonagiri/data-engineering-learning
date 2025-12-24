def transform_currency(amount, rate):
    """
    Simple function to convert currency.
    In a real project, this would be complex DataFrame logic.
    """
    if amount < 0:
        raise ValueError("Amount cannot be negative")
    return round(amount * rate, 2)

def clean_name(name):
    """
    Removes whitespace and capitalizes.
    """
    if not name:
        return "Unknown"
    return name.strip().title()
