import math

BASE_COST = 40
EXTRA_KG_COST = 15
SAME_CITY_DISCOUNT_PERCENT = 20


def delivery_cost(weight_kg, same_city):
    if isinstance(weight_kg, bool) or not isinstance(weight_kg, (int, float)):
        raise ValueError("weight_kg must be a number")
    if not math.isfinite(weight_kg) or weight_kg <= 0:
        raise ValueError("weight_kg must be a positive finite number")
    if not isinstance(same_city, bool):
        raise ValueError("same_city must be a bool")

    extra_full_kg = max(0, math.floor(weight_kg - 1))
    total = BASE_COST + EXTRA_KG_COST * extra_full_kg
    if same_city:
        total = total * (100 - SAME_CITY_DISCOUNT_PERCENT) // 100
    return total
